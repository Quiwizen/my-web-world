#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def get_available_filename(base_name="gallery-detail.html"):
    """
    获取可用的文件名，如果文件已存在则自动递增编号
    
    :param base_name: 基础文件名
    :return: 可用的文件名
    """
    # 分离文件名和扩展名
    name, ext = os.path.splitext(base_name)
    
    # 检查基础文件名是否存在
    if not os.path.exists(base_name):
        return base_name
    
    # 如果存在，尝试递增编号
    counter = 2
    while True:
        new_name = f"{name}{counter}{ext}"
        if not os.path.exists(new_name):
            return new_name
        counter += 1

def generate_gallery_detail(image_urls, title="作品集详情", output_file="gallery-detail.html"):
    """
    生成 gallery-detail.html 文件
    
    :param image_urls: 图片 URL 数组
    :param title: 作品集标题
    :param output_file: 输出文件名
    """
    num_images = len(image_urls)
    
    # 生成缩略图按钮 HTML
    thumbnail_buttons = ""
    for i, url in enumerate(image_urls):
        active_class = "border-primary" if i == 0 else "border-transparent hover:border-neutral-300"
        loading_attr = "loading=\"eager\"" if i == 0 else "loading=\"lazy\""
        thumbnail_buttons += f"""            <button class="thumbnail-btn flex-shrink-0 w-full rounded-md overflow-hidden border-2 {active_class}" data-index="{i}">
              <img src="{url}" alt="{i+1}" class="w-full h-full object-cover" {loading_attr}>
            </button>
"""
    
    # 生成 JavaScript 图片数组
    js_images = "        const images = [\n"
    for url in image_urls:
        js_images += f"          '{url}',\n"
    js_images += "        ];"
    
    # HTML 模板
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>图集详情 | 小崔</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="tailwind-config.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/lucide@latest"></script>
  <style type="text/tailwindcss">@import "gallery-detail.css";</style>
</head>
<body>
  <!-- 返回按钮 -->
  <nav class="fixed top-0 left-0 w-full z-50 bg-white/80 backdrop-blur-md shadow-soft">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <a href="index.html#gallery" class="flex items-center gap-2 text-neutral-700 hover:text-primary transition-colors back-btn">
          <i data-lucide="arrow-left" class="w-5 h-5"></i>
          <span>返回作品集</span>
        </a>
        <!-- 标题和图片数 -->
        <div class="text-center">
          <h1 class="text-lg font-bold text-neutral-900">{title}</h1>
          <p class="text-xs text-neutral-500">共 {num_images} 张图片</p>
        </div>
        <!-- 占位符保持居中 -->
        <div class="w-28"></div>
      </div>
    </div>
  </nav>

  <!-- 主图展示区 -->
    <section class="pt-20 pb-6 bg-neutral-100">
      <div class="max-w-6xl mx-auto px-4 flex flex-col lg:flex-row items-start gap-6">
        <!-- 左侧主图区域 -->
        <div class="flex-1 flex flex-col items-center w-full">
          <!-- 图片展示 -->
          <div class="relative rounded-lg overflow-hidden shadow-soft mb-6 portrait-container w-full max-w-2xl" id="imageContainer">
            <img id="mainImage" src="{image_urls[0] if image_urls else ''}" alt="image" loading="eager">
            <!-- 左侧悬浮导航按钮 -->
            <button id="floatPrevBtn" class="float-nav-btn absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-black/50 hover:bg-black/70 rounded-full flex items-center justify-center text-white shadow-lg" disabled>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </button>
            <!-- 右侧悬浮导航按钮 -->
            <button id="floatNextBtn" class="float-nav-btn absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-black/50 hover:bg-black/70 rounded-full flex items-center justify-center text-white shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
          </div>

          <!-- 导航按钮 -->
          <div class="flex justify-center items-center gap-4">
            <button id="prevBtn" class="nav-btn px-4 py-2 rounded-md border border-neutral-200 disabled" disabled>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </button>
            <span id="counter" class="text-neutral-500">1 / {num_images}</span>
            <button id="nextBtn" class="nav-btn px-4 py-2 rounded-md border border-neutral-200">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
          </div>
        </div>

        <!-- 右侧缩略图区域 -->
        <div class="w-20 lg:w-24 flex-shrink-0">
          <!-- 缩略图导航 - 纵向排列 -->
          <div class="flex flex-col gap-2 overflow-y-auto max-h-[70vh]" id="thumbnailContainer">
{thumbnail_buttons}          </div>
        </div>
      </div>
    </section>

  <!-- 页脚 -->
  <footer class="py-4 bg-neutral-900 text-center">
    <p class="text-neutral-500 text-xs">© 2026 小崔Stdio</p>
  </footer>

  <script>
    // 页面加载完成后执行
    document.addEventListener('DOMContentLoaded', function() {{
      // 图片数组
{js_images}

      const mainImage = document.getElementById('mainImage');
      const prevBtn = document.getElementById('prevBtn');
      const nextBtn = document.getElementById('nextBtn');
      const floatPrevBtn = document.getElementById('floatPrevBtn');
      const floatNextBtn = document.getElementById('floatNextBtn');
      const counter = document.getElementById('counter');
      const thumbnailBtns = document.querySelectorAll('.thumbnail-btn');

      let currentIndex = 0;

      function updateImage() {{
        mainImage.src = images[currentIndex];
        counter.textContent = (currentIndex + 1) + ' / ' + images.length;
        
        // 更新缩略图选中状态
        thumbnailBtns.forEach(function(btn, index) {{
          if (index === currentIndex) {{
            btn.classList.add('border-primary');
            btn.classList.remove('border-transparent');
            // 自动滚动到当前选中的缩略图
            btn.scrollIntoView({{
              behavior: 'smooth',
              block: 'nearest',
              inline: 'center'
            }});
          }} else {{
            btn.classList.remove('border-primary');
            btn.classList.add('border-transparent');
          }}
        }});

        // 更新按钮状态
        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex === images.length - 1;
        floatPrevBtn.disabled = currentIndex === 0;
        floatNextBtn.disabled = currentIndex === images.length - 1;
      }}

      // 下一张
      function goNext() {{
        if (currentIndex < images.length - 1) {{
          currentIndex++;
          updateImage();
        }}
      }}

      // 上一张
      function goPrev() {{
        if (currentIndex > 0) {{
          currentIndex--;
          updateImage();
        }}
      }}

      // 绑定事件
      prevBtn.addEventListener('click', goPrev);
      nextBtn.addEventListener('click', goNext);
      floatPrevBtn.addEventListener('click', goPrev);
      floatNextBtn.addEventListener('click', goNext);

      // 缩略图点击事件
      thumbnailBtns.forEach(function(btn, index) {{
        btn.addEventListener('click', function() {{
          currentIndex = index;
          updateImage();
        }});
      }});

      // 键盘导航
      document.addEventListener('keydown', function(e) {{
        // 阻止方向键、Home、End 的默认滚动行为
        if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) {{
          e.preventDefault();
        }}
        
        if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A' || e.key === 'ArrowUp') {{
          goPrev();
        }}
        if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D' || e.key === 'ArrowDown') {{
          goNext();
        }}
        if (e.key === 'Home') {{
          currentIndex = 0;
          updateImage();
        }}
        if (e.key === 'End') {{
          currentIndex = images.length - 1;
          updateImage();
        }}
      }});

      // 初始化显示第一张图
      updateImage();
    }});
  </script>
</body>
</html>
"""
    
    # 获取可用的文件名
    available_file = get_available_filename(output_file)
    
    # 写入文件
    with open(available_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Successfully generated {available_file} with {num_images} images.")


if __name__ == "__main__":
    # ========== 配置参数 ==========
    # 图集名称
    gallery_title = "bm 活底披萨烤盘"
    
    # 图片 URL 数组
    images = [
       'https://i.ibb.co/SD9v0Jrw/26.jpg',
       'https://i.ibb.co/RkYVsnwM/25.jpg',
       'https://i.ibb.co/yT3Vf7M/24.jpg',
       'https://i.ibb.co/hx8RCjZm/23.jpg',
       'https://i.ibb.co/rTc3gmV/22.jpg',
       'https://i.ibb.co/hF1Tfdc8/21.jpg',
       'https://i.ibb.co/twQrDVt8/20.jpg',
       'https://i.ibb.co/Kz85vD3Q/19.jpg',
       'https://i.ibb.co/3yTS0hQX/18.jpg',
       'https://i.ibb.co/VpvqrbL4/16.jpg',
       'https://i.ibb.co/4RhdvFCf/17.jpg',
       'https://i.ibb.co/jYgVhXH/15.jpg',
       'https://i.ibb.co/Cp27JFgZ/14.jpg',
       'https://i.ibb.co/ymSByj25/13.jpg',
       'https://i.ibb.co/hJqBf8Vx/12.jpg',
       'https://i.ibb.co/h1mTYHd7/11.jpg',
       'https://i.ibb.co/WvnQvyYz/10.jpg',
       'https://i.ibb.co/0pDJWdBs/9.jpg',
       'https://i.ibb.co/pvF9QP6W/8.jpg',
       'https://i.ibb.co/fdZ5wKCs/7.jpg',
       'https://i.ibb.co/v4R4hJYq/6.jpg',
       'https://i.ibb.co/gFhY6f8Q/4.jpg',
       'https://i.ibb.co/zhGZHsY1/5.jpg',
       'https://i.ibb.co/ZpS8YH2j/3.jpg',
       'https://i.ibb.co/zTV78DM6/2.jpg',
       'https://i.ibb.co/qFCBpfhL/image.jpg',
       'https://i.ibb.co/kg1yJDJk/1.jpg',
    ]
    
    # 自动统计图片数量
    num_images = len(images)
    print(f"图集名称: {gallery_title}")
    print(f"图片数量: {num_images} 张")
    
    # 生成 gallery-detail.html
    generate_gallery_detail(images, title=gallery_title)