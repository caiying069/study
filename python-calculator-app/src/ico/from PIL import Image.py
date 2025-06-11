from PIL import Image
 
# 打开PNG图像
png_image = Image.open("python-calculator-app\src\caaculator.png")
 
# 创建一个ICO对象，并添加原始图像（通常你需要指定不同尺寸的图像以符合ICO规范）
# 例如，创建一个包含32x32和16x16尺寸图像的ICO文件
ico = Image.open("python-calculator-app\src\caaculator.png")
ico.save("output.ico", format='ICO', sizes=[(32, 32), (16, 16)])