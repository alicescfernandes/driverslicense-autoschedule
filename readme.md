# What is this?

During COVID i started to take my drivers license, and in Portugal, for you to be able to do the road test, you need to first have 16 theory classes before you can go start to take practice lessons on a car. For those theory classes, during covid, you could only book them by sending an email to the drivers school or by calling. I work full time, so by the time i was able to check the theory classes schedule, some classes were already fully booked by other students.

So, my solution was to develop a bot, that ran inside a Raspberry Pi 3, that did the scheduling for me, by email. Now that i was able to complete my driving license program, i now feel safe to share this little hacky cool project.

## How did this worked?

My driving school publishes a PDF with the schedule for the month, and i know what classes i have missing, and i also have an email account. So the steps are:

1. Download the PDF from the website
2. Parse the PDF (with `tabula`) into data that can be worked with
3. Find all classes that are happening at a given hour for the month (with `pandas`)
4. Of all of the classes above, find the ones that i still need to take
    1. My school had a restriction where i could only book 3 per month during COVID
5. Send a beautiful email to the school to book those classes (with `smtplib`)
6. After the email mark those classes as booked internally, and i used Google Sheets and `gspread` because i could see the spreadsheet on my phone, but also tried a SQLite database
7. Job done, i can now not worry too much about booking classes

I eventually ran this inside docker because my RasPi had a lot of cool stuff running, and it was great to stop code from messing with other code

## Did this worked?

Yes! I only finished this a little bit before finishing the theory classes, so it didn't had much use, but it did send some emails

### Config keys

This project needs some configurations that are kept out for safety, so take a look at the sample-env to see what keys i'm talking about

### Spreadsheet

I've put a spreadsheet that has the format that was used on this project. The data is gone, but it was that template, and it was online, on Google Sheets
