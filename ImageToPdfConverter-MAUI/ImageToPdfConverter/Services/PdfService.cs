﻿using ImageToPdfConverter.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Maui.Graphics;
using Microsoft.Maui.Graphics.Skia;
using SkiaSharp;

namespace ImageToPdfConverter.Services
{
    public class PdfService
    {
        public async Task<string> CreatePdfFromImagesAsync(List<string> imagePaths, string fileName)
        {
            // Определяем путь для сохранения PDF
            string pdfDirectory = Path.Combine(FileSystem.CacheDirectory, "PDFs");
            if (!Directory.Exists(pdfDirectory))
                Directory.CreateDirectory(pdfDirectory);

            string pdfPath = Path.Combine(pdfDirectory, fileName);

            // Создаем PDF документ с использованием SkiaSharp
            using (var stream = new SKFileWStream(pdfPath))
            {
                // Создаем документ с настройками PDF
                using (var document = SKDocument.CreatePdf(stream))
                {
                    foreach (var imagePath in imagePaths)
                    {
                        using (var bitmap = SKBitmap.Decode(imagePath))
                        {
                            // Стандартный размер страницы A4
                            float pageWidth = 8.27f * 72; // 8.27 inches * 72 dpi = 595 points (стандарт в PDF)
                            float pageHeight = 11.69f * 72; // 11.69 inches * 72 dpi = 842 points

                            // Создаем страницу
                            var pageCanvas = document.BeginPage(pageWidth, pageHeight);

                            // Заполняем фон белым цветом (для PNG с прозрачностью)
                            using (var paint = new SKPaint { Color = SKColors.White })
                            {
                                pageCanvas.DrawRect(0, 0, pageWidth, pageHeight, paint);
                            }

                            // Вычисляем размеры для масштабирования с сохранением пропорций
                            float scaleX = pageWidth / bitmap.Width;
                            float scaleY = pageHeight / bitmap.Height;
                            float scale = Math.Min(scaleX, scaleY) * 0.9f; // Оставляем небольшие поля

                            float scaledWidth = bitmap.Width * scale;
                            float scaledHeight = bitmap.Height * scale;

                            // Центрируем изображение
                            float x = (pageWidth - scaledWidth) / 2;
                            float y = (pageHeight - scaledHeight) / 2;

                            // Создаем прямоугольник для отрисовки
                            var rect = new SKRect(x, y, x + scaledWidth, y + scaledHeight);

                            // Отрисовываем изображение
                            pageCanvas.DrawBitmap(bitmap, rect);

                            // Завершаем страницу
                            document.EndPage();
                        }
                    }
                }
            }

            // Сохраняем PDF в галерею или другое постоянное хранилище
            string destinationPath = await SavePdfToPublicStorageAsync(pdfPath, fileName);
            return destinationPath;
        }
        private async Task<string> SavePdfToPublicStorageAsync(string sourcePath, string fileName)
        {
            try
            {
                // Получаем путь для сохранения в общедоступную папку
                string targetPath;

                if (DeviceInfo.Platform == DevicePlatform.Android)
                {
                    // Для Android используем MediaStore API через FileSystem
                    targetPath = Path.Combine(FileSystem.AppDataDirectory, fileName);
                    File.Copy(sourcePath, targetPath, true);
                }
                else if (DeviceInfo.Platform == DevicePlatform.iOS)
                {
                    // Для iOS используем папку Documents
                    targetPath = Path.Combine(FileSystem.AppDataDirectory, fileName);
                    File.Copy(sourcePath, targetPath, true);
                }
                else
                {
                    // Для других платформ просто возвращаем исходный путь
                    targetPath = sourcePath;
                }

                return targetPath;
            }
            catch (Exception ex)
            {
                throw new Exception($"Не удалось сохранить PDF файл: {ex.Message}");
            }
        }
    }
}