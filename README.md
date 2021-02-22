# Parser for Logos from www.brandsoftheworld.com

This repository contains parser that downloads logos from www.brandsoftheworld.com and puts them into a directory, where each subfolder represents different category. Full download will take several hours and provide you with around 180k logos.

# Minimal Examples:

Download all available logos (180k) in all available categories. Required argument: target directory.

```.bash
python logo_parse.py /home/yourpcname/Desktop/logo_parser/logo_data
```
Download n first pages of all categories. Optional argument --max_pages: number of pages to download in each category (32 logos on one page). Default - 1000.

```.bash
python logo_parse.py /home/yourpcname/Desktop/logo_parser/logo_data --max_pages 1
```

Download logos for the categories of interest. Optional argument --categories: categories of interest, by default downloads from all categories. Use --help to see availble categories.

```.bash
python logo_parse.py /home/yourpcname/Desktop/logo_parser/logo_data --max_pages 1 --categories Government Heraldry Military
```

Run --help

```.bash
python logo_parse.py /home/yourpcname/Desktop/logo_parser/logo_data --help
```

# Sample Logos:
![Sample Logos](https://github.com/nslyubaykin/logos_parser/blob/master/sample_logos.png)
