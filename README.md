# yande-crawler
## 中文版说明(Chinese version)
在一次偶然的学习（moyu）中，我发现了yande这个神奇的网站，它涵盖图像之多令我如痴如醉，免费下载高清图像的功能令我无法自拔。我与它相见恨晚。当然，它也不是完美的，那就是它的美图实在太多了，一个一个点击下载实在是太费手了。古人云：“在处理黄色信息时，人的创作力和创作热情总是无穷的”。为了脱离低级的lsp而成为一个高级的lsp，我开发了自动并行化下载的爬虫，经过实验亲测有效。虽然也不指望大家用，但是也可以作为我手滑删掉的备份。

### 提示
代码还处在完善阶段，目前仅具备基本使用功能，GUI、中断与继续等功能正在开发中。敬请期待下一步的开发。

### 使用方法
在if __name__ == '__main__'下输入Pic_crawler(##要爬图像的tag, ##要爬的页数（如果不指定，代码会自动检测，但是受限于网速，结果不一定精确）, ##保存图像的路径文件夹, ##保存时文件名的前缀)
### 例：
Pic_crawler('izumi_sagiri', 16, r'D:\file\Pictures\yande', 'yande')  # 没错，和泉纱雾我老婆

## English version README
I found yande, an awesome website by accident. I was fascinated by its collection and the function to download high-resolution pictures for free. I regarded it a shame that I didn't find it earlier. However, this website is definitely not a perfect one as it's troublesome to download so many beautiful images one by one manually. As ancient ancestors in China said, 'Humans are ultra creative and enthusiastic when dealing with pornographic information'(this is fabricated by me, a typical Chinese joke). To make myself not just a perverted man, but a skillful perverted man, I developed this project, an simple but useful distributed auto crawler for this website. I tested its effectiveness by myself. I just upload it as a backup in case I undeliberately delete the code.

### Hint
This project is under developing now. Only basic functions can be used currently. Other functions including GUI, pausing downloading and so on are being developed. Please look forward to it. 

### How to use
Currently, the code is not perfect. It can only be used by adding Pic_crawler(## the tag in yande you want to get, ##number of pages you want to download(if you don't give a number, the code itself can detect the maximum number, not quite accurate though), ##the dir that you want to download the images into, make sure it's empty, ##the prefix of downloaded pictures' file name)
### Example:
Pic_crawler('izumi_sagiri', 16, r'D:\file\Pictures\yande', 'yande')
