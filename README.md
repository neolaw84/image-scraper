# image-scraper

To download images from online galleries using simple directory structure

# Change Log

* 2021-08-05 : MVP
  * Minimum config
  * Site with pagination
  * Each page has multiple sub-pages (model pages)
  * Each model page has multiple sibling-pages 
  * Each model page has links to images
  * Produces url to uuid table as meta data
  * Delays randomly

* 2021-08-06 : Check if downloaded
  * Check in the meta file if it is downloaded
  * Append to meta file accordingly
  * Replace config with easydict