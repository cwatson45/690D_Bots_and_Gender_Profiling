import os
import cv2
import xml.etree.cElementTree as ET
import xml.dom.minidom

def readImgShape(imgFile):
	img = cv2.imread(imgFile, 0)
	return img.shape

def readImgSize(imgFile):
	return cv.GetSize(imgFile)

def getObjCoordinates(txt_path):
	with open(txt_path, "r") as f:
		ln = f.readline()
		rets = []
		cnt = 0
		while len(ln) > 0:
			divs = ln.split(" ")
			#print(ln)
			ln = f.readline()
			if divs[0] != "people" and divs[0] != "person" and divs[0] != "person?" and divs[0] != "cyclist":
				if cnt > 0:
					raise Exception(divs[0])
				continue
			val = {}
			val["name"] = divs[0]
			val["xmin"] = divs[1]
			val["ymin"] = divs[2]
			val["xmax"] = str(int(val["xmin"]) + int(divs[3]) - 1)
			val["ymax"] = str(int(val["ymin"]) + int(divs[4]) - 1)
			val["occlusion"] = divs[5]
			for idx in range(6, len(divs)):
				if int(divs[idx]) != 0:
					#print(divs)
					#print(txt_path)
					raise Exception("Something is not zero " + ln)
			#print(val)
			rets.append(val)
			cnt += 1
		return rets
cnt = 0

def test(val, lim, st, img_pt):
	if int(val) < 1 or int(val) > int(lim):
		raise Exception("Some error occured in " + st + " : " + str(val) + " " + str(lim) + " " + img_pt)
def convert_text_to_xml(txt_path, img_path, xml_path, img_folder, img_name):
	global cnt
	annotation = ET.Element("annotation")
	folder = ET.SubElement(annotation, "folder")
	folder.text = img_folder
	filename = ET.SubElement(annotation, "filename")
	filename.text =img_name
	path = ET.SubElement(annotation, "path")
	path.text = img_path
	source = ET.SubElement(annotation, "source")
	database = ET.SubElement(source, "database")
	database.text = "kaist multispectral dataset"

	img_shape = readImgShape(img_path)

	size = ET.SubElement(annotation, "size")
	width = ET.SubElement(size, "width")
	height = ET.SubElement(size, "height")
	depth = ET.SubElement(size, "depth")

	width.text = str(img_shape[1])
	height.text = str(img_shape[0])

	if len(img_shape) > 2:
		depth.text = str(img_shape[2])
	else:
		depth.text = "1"
	segmented = ET.SubElement(annotation, "segmented")
	segmented.text = "0"
	#print(cnt)
	objs = getObjCoordinates(txt_path)
	#print(len(objs))

	for obj in objs:
		curObj = ET.SubElement(annotation, "object")
		nm = ET.SubElement(curObj, "name")
		nm.text = obj["name"]
		pose = ET.SubElement(curObj, "pose")
		pose.text = "Unspecified"
		truncated = ET.SubElement(curObj, "truncated")
		truncated.text = "0"
		occluded = ET.SubElement(curObj, "occluded")
		occluded.text = obj["occlusion"]
		difficult = ET.SubElement(curObj, "difficult")
		difficult.text = "0"
		bndbox = ET.SubElement(curObj, "bndbox")
		xmin = ET.SubElement(bndbox, "xmin")
		xmax = ET.SubElement(bndbox, "xmax")
		ymin = ET.SubElement(bndbox, "ymin")
		ymax = ET.SubElement(bndbox, "ymax")
		xmin.text = obj["xmin"]
		xmax.text = obj["xmax"]
		ymin.text = obj["ymin"]
		ymax.text = obj["ymax"]
		test(xmin.text, width.text, "width", img_path)
		test(xmax.text, width.text, "width", img_path)
		test(ymin.text, height.text, "height", img_path)
		test(ymax.text, height.text, "height", img_path)


	#boxes = getObjCoordinates(txt_path)
	st = ET.tostring(annotation, encoding='utf8', method='xml')
	dom = xml.dom.minidom.parseString(st)
	#print(dom.toprettyxml())
	with open(xml_path, "w+") as wout:
		wout.write(dom.toprettyxml())
		print("wrote to " + xml_path)
	#exit(0)
	#if len(objs) > 0:
		#print(st)
	cnt = cnt + 1
	print(cnt)



if __name__ == "__main__":

	cDir = os.getcwd()

	annotations_dir = "annotations"

	annotations_dir = os.path.join(cDir, annotations_dir)

	image_dir = "images"

	image_dir = os.path.join(cDir, image_dir)

	pascal_anno = "pascal_annotations"

	pascal_anno = os.path.join(cDir, pascal_anno)

	if not os.path.exists(pascal_anno):
		os.makedirs(pascal_anno)

	dirs = os.listdir(annotations_dir)

	for dirr in dirs:
		full_dir = os.path.join(annotations_dir, dirr)

		if not os.path.isdir(full_dir):
			continue

		pascal_dir = os.path.join(pascal_anno, dirr)

		if not os.path.exists(pascal_dir):
			os.makedirs(pascal_dir)
		cur_image_dir = os.path.join(image_dir, dirr)

		vdirs = os.listdir(full_dir)

		for vdir in vdirs:
			txtdir = os.path.join(full_dir, vdir)
			if not os.path.isdir(txtdir):
				continue
			pascal_vdir = os.path.join(pascal_dir , vdir)

			if not os.path.exists(pascal_vdir):
				os.makedirs(pascal_vdir)

			imgdir = os.path.join(cur_image_dir, vdir + "/lwir") 

			annos = os.listdir(txtdir)

			for anno in annos:
				if not anno.endswith(".txt"):
					continue
				xml_fl = anno[:-3]
				xml_path = os.path.join(pascal_vdir, xml_fl + "xml")
				txt_path = os.path.join(txtdir, anno)
				img_path = os.path.join(imgdir, xml_fl + "jpg")
				if not os.path.exists(txt_path):
					raise Exception("Text annontation doesn't exists for " + txt_path)
				if not os.path.exists(img_path):
					raise Exception("Image doesn't exist for " + img_path)
				#print(xml_path)
				#print(txt_path)
				#print(img_path)
				#readImg(imgpath)
				convert_text_to_xml(txt_path, img_path, xml_path, imgdir, xml_fl + "jpg")

