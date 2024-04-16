# AutoCert

A Python script which takes volunteer data as input and generates leaving certificates.

On leaving Edinburgh Nightline, volunteers receive a certificate which details their various contributions. These are formulaic by design,  but creating them by hand still takes a significant chunk of time. The script automates this task, taking [Three Rings](https://www.3r.org.uk/stats/number_of_shifts) CSV export data and creating a folder of PDF certificates through [md2pdf](https://pypi.org/project/md2pdf/). The [example](data.csv) is in the required CSV format and produces PDFs [like this](Certs/Azhar_Ó_Cléirigh.pdf)

Much of this script is specific to Edinburgh Nightline (e.g. shift names). That said, if modified it could work for other Nightlines or even other data from elsewhere. Generally, it's an example of automated document generation in Python using `md2pdf`.

The Python and CSS are MIT licensed, released without warranty. The [logo](Img/logo.jpg) is copyright of [Edinburgh Nightline](https://ednightline.com/) and may not be used or modified without permission. The two signatures ([1](https://commons.wikimedia.org/wiki/File:Hristo_Tsanev_Signature_%28transparent%29.png), [2](https://commons.wikimedia.org/wiki/File:Signature_YA.png)) are from Wikimedia and are [CC0](https://creativecommons.org/publicdomain/zero/1.0) and [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0) licensed respectively. The example included is real Three Rings export data, but with [random names](https://www.behindthename.com/random/random.php), purged emails, and attribution randomised.
