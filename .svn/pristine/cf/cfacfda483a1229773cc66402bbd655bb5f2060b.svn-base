from PIL import Image
import ImageEnhance

im = Image.open("captcha.jpg")
nx, ny = im.size
im2 = im.resize((int(nx*5), int(ny*5)), Image.BICUBIC)
im2.save("final_pic.png")
enh = ImageEnhance.Contrast(im)
enh.enhance(1.3).show("30% more contrast")
