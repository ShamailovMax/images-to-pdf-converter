using ImageToPdfConverter.Models;
using ImageToPdfConverter.Services;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Storage;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

namespace ImageToPdfConverter.ViewModels
{
    public class MainViewModel : INotifyPropertyChanged
    {
        private readonly PdfService _pdfService;
        private ImageItem _selectedImage;
        private bool _isBusy;
        private string _statusMessage;

        public ObservableCollection<ImageItem> Images { get; } = new ObservableCollection<ImageItem>();

        public ImageItem SelectedImage
        {
            get => _selectedImage;
            set
            {
                _selectedImage = value;
                OnPropertyChanged();
            }
        }

        public bool IsBusy
        {
            get => _isBusy;
            set
            {
                _isBusy = value;
                OnPropertyChanged();
                // При изменении IsBusy обновляем доступность команд
                (AddImagesCommand as Command)?.ChangeCanExecute();
                (RemoveImageCommand as Command)?.ChangeCanExecute();
                (CreatePdfCommand as Command)?.ChangeCanExecute();
            }
        }

        public string StatusMessage
        {
            get => _statusMessage;
            set
            {
                _statusMessage = value;
                OnPropertyChanged();
            }
        }

        public ICommand AddImagesCommand { get; }
        public ICommand RemoveImageCommand { get; }
        public ICommand CreatePdfCommand { get; }

        public MainViewModel()
        {
            _pdfService = new PdfService();

            AddImagesCommand = new Command(async () => await AddImagesAsync(), () => !IsBusy);
            RemoveImageCommand = new Command<ImageItem>(RemoveImage, (item) => !IsBusy && item != null);
            CreatePdfCommand = new Command(async () => await CreatePdfAsync(), () => !IsBusy && Images.Count > 0);
        }

        private async Task AddImagesAsync()
        {
            try
            {
                IsBusy = true;
                StatusMessage = "Выбор изображений...";

                var options = new PickOptions
                {
                    PickerTitle = "Выберите изображения",
                    FileTypes = FilePickerFileType.Images
                };

                var results = await FilePicker.PickMultipleAsync(options);

                if (results != null && results.Any())
                {
                    foreach (var result in results)
                    {
                        var imageItem = new ImageItem
                        {
                            FilePath = result.FullPath,
                            FileName = result.FileName,
                            ImageSource = ImageSource.FromFile(result.FullPath)
                        };
                        Images.Add(imageItem);
                    }
                    StatusMessage = $"Добавлено {results.Count()} изображений.";
                }
                else
                {
                    StatusMessage = "Изображения не выбраны.";
                }
            }
            catch (Exception ex)
            {
                StatusMessage = $"Ошибка при добавлении изображений: {ex.Message}";
            }
            finally
            {
                IsBusy = false;
            }
        }

        private void RemoveImage(ImageItem item)
        {
            if (item != null)
            {
                Images.Remove(item);
                if (SelectedImage == item)
                    SelectedImage = null;

                StatusMessage = "Изображение удалено.";
            }
        }

        private async Task CreatePdfAsync()
        {
            if (Images.Count == 0)
            {
                StatusMessage = "Нет изображений для создания PDF.";
                return;
            }

            try
            {
                IsBusy = true;
                StatusMessage = "Создание PDF...";

                // Запрос имени файла
                string defaultFileName = "Images" + DateTime.Now.ToString("_yyyyMMdd_HHmmss") + ".pdf";
                string fileName = await Application.Current.MainPage.DisplayPromptAsync(
                    "Имя файла",
                    "Введите имя PDF файла:",
                    initialValue: defaultFileName);

                if (string.IsNullOrEmpty(fileName))
                {
                    StatusMessage = "Создание PDF отменено.";
                    return;
                }

                if (!fileName.EndsWith(".pdf", StringComparison.OrdinalIgnoreCase))
                    fileName += ".pdf";

                // Получаем пути к изображениям
                var imagePaths = Images.Select(i => i.FilePath).ToList();

                // Создаем PDF
                string pdfPath = await _pdfService.CreatePdfFromImagesAsync(imagePaths, fileName);

                StatusMessage = $"PDF создан успешно. Вы можете поделиться файлом или сохранить его.";

                // Спрашиваем пользователя, хочет ли он открыть файл сразу
                // Заменить строчку
                bool shouldShare = await Application.Current.MainPage.DisplayAlert(
                    "PDF создан",
                    $"PDF файл успешно создан. Хотите сохранить его сейчас?",
                    "Да", "Нет");

                if (shouldShare)
                {
                    // Убираем присвоение результата
                    await Share.Default.RequestAsync(new ShareFileRequest
                    {
                        Title = "Сохранить PDF как...",
                        File = new ShareFile(pdfPath)
                    });
                }
            }
            catch (Exception ex)
            {
                StatusMessage = $"Ошибка при создании PDF: {ex.Message}";
            }
            finally
            {
                IsBusy = false;
            }
        }
        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}