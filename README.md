# CheckGradeOpenu
A simple python selenium program to check and alert the user when test grade is entered @ OpenU, With logging & Command line arguments configuration
## Dependencies
* Python 3.6+
* Selenium module for python
## Usage
```
py main.py main.py [-h] [--sleep SLEEP] --userName USERNAME --pwd PWD --id ID
  --course COURSE --semester SEMESTER --group GROUP --center CENTER
```
### Arguments:
##### optional arguments:
*  `-h, --help`            show this help message and exit
*  `--sleep SLEEP, -s SLEEP`
                        The time to wait before initiating another request.

##### Credentials - REQUIRED:
*  `--userName USERNAME`   Your user name
*  `--pwd PWD`             Your password
*  `--id ID`               Your ID number

##### Course Information - REQUIRED:
*  `--course COURSE`       Course number, such as 20109 or 04101
*  `--semester SEMESTER`   Semester, Formatted as yyyy[a|b|c] (e.g. 2021a)
*  `--group GROUP`         Group number (e.g. 81)
*  `--center CENTER`       Teaching center number (e.g. 780)
