init:
	sudo apt install poppler-utils poppler-data
	pip3 install -r requirements.txt
run:
	python3 -m pdf2notion
test:
	echo "未定義"
