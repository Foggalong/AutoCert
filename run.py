#!/usr/bin/env python3

from csv import DictReader      # loading data file
from datetime import datetime   # calculating time volunteered
from md2pdf.core import md2pdf  # converting markdown to PDF


# user variables, all that needs changing in this script
coord1 = " Zoë Goodwin"
coord2 = " Álvaro Bermúdez"
today = "DD/MM/YYYY"
year = "20XX/YY"


def volunteerList(filename):
    """
    Takes the name of a CSV file as string input and returns a
    list of dictionaries, one item for each line in the file.
    """
    with open(filename) as csvFile:
        return list(DictReader(csvFile))


def volunteerPronoun(strFriendlyName):
    """
    Takes a volunteers Three Rings friendly name as string input
    and returns their pronoun as string output.
    """
    knownPronouns = ["he", "she", "they", "xe"]
    try:
        str3R = strFriendlyName.split("(")[1].split("/")[0].lower()
        if str3R not in knownPronouns:
            raise IndexError
        return str3R.capitalize()
    except IndexError:
        return "They"


def durationString(strJoined, strLeft):
    """
    Take a volunteers start date and end date as strings in
    DD/MM/YYYY format and return a string giving how long they
    volunteered for.
    """
    # calculate how many days volunteered
    dateJoined = datetime.strptime(strJoined, '%d/%m/%Y')
    dateLeft = datetime.strptime(strLeft, '%d/%m/%Y')
    daysVolunteered = (dateLeft-dateJoined).days
    # if volunteered less than 18 months (540 days) give in months
    if daysVolunteered <= 540:
        duration = round(daysVolunteered/30)
        units = "month"
    else:
        duration = round(daysVolunteered/365)
        units = "year"
    # pluralise if needed
    if duration != 1:
        units += "s"
    # return final string
    return f"{duration} {units}"


def shiftsString(strShort, strLong, strRemote):
    """
    Takes the number of each type of shift a volunteer has done
    as a string and returns a string for the letter.
    """
    stringSegments = []
    # craft string segment for overnight shifts
    intOvernight = int(strLong)
    if intOvernight > 0:
        strOvernight = f"{intOvernight} overnight shift"
        # work out if to pluralise
        if intOvernight > 1:
            strOvernight += "s"
        stringSegments.append(strOvernight)
    # craft string segment for evening shifts
    intEvening = int(strShort) + int(strRemote)
    if intEvening > 0:
        strEvening = f"{intEvening} evening shift"
        # work out if to pluralise
        if intEvening > 1:
            strEvening += "s"
        stringSegments.append(strEvening)
    # combine two parts together
    return " and ".join(stringSegments)


def shiftHours(strShort, strLong, strRemote):
    """
    Takes the number of each type of shift a volunteer has done
    as a string and returns the number of hours they equates to
    as an integer.
    """
    # don't need to worry about pluralising, can't be less than 4
    return 12*int(strLong) + 4*(int(strShort)+int(strRemote))


def ongoingString(strOngoing):
    """
    Takes the number of ongoing trainings done as a string and if
    non-zero returns a string for the letter.
    """
    if int(strOngoing) > 0:
        return (" Those skills were kept up to date through completing "
                "ongoing training throughout their time volunteering.")
    else:
        return ""


def supportString(strEmergency, strDropIn, strOnCall, pronoun="they"):
    """
    Takes the number of support shifts (office drop-in, on-call
    welfare, and emergency contact) as string inputs and returns
    a string for the letter; the string will be empty if they did
    no such shifts.
    """
    intSupport = int(strEmergency) + int(strDropIn) + int(strOnCall)
    if intSupport > 0:
        string = f" {pronoun} also completed {intSupport} support"
        # check if need to pluralise
        if intSupport > 1:
            string += " shifts"
        else:
            string += " shift"
        string += ", aiding the call taking volunteers."
        return string
    else:
        return ""


def committeeString(strCommittee, pronoun="they"):
    """
    Takes a comma separated list-string of the committee roles
    a volunteer had as input and returns a string for the letter;
    the string will be empty if they never held a committee role.
    """
    # if held no roles return a blank string
    if strCommittee == "":
        return ""
    # if held 1 role we've nothing to replace
    if strCommittee.count(", ") == 0:
        committeeRoles = strCommittee
    # if held 2 roles replace comma with 'and'
    if strCommittee.count(", ") == 1:
        committeeRoles = strCommittee.replace(", ", " and ")
    # if held 3 or more roles, replace last comma with ', and '
    elif strCommittee.count(", ") > 1:
        committeeRoles = ", and ".join(strCommittee.rsplit(", ", 1))
    # format and return final string
    return (f" {pronoun} also went beyond this and has "
            f"served on our committee as {committeeRoles}.")


# MAIN

# markdown-formatted multiline string which forms the letter
letter = """\
<img class="logo" title="Edinburgh Nightline"
     alt="Nightline logo" src="Img/logo.jpg">
<div style="clear: right">
<br><br><br>
<p style="text-align:right;">{today}</p>

To whom it may concern,

We hereby confirm that {firstname} {lastname} was a Listening Volunteer at \
Edinburgh Nightline for {duration}, from {joined} to {left}. \
{pronoun} completed extensive active listening training and has \
an awareness of issues related to mental health.{ongoing}

{firstname} contributed to Edinburgh Nightline by signing up for regular \
shifts to run our listening and information service, covering students \
across Edinburgh. {pronoun} completed {shifts}, totalling {hours} hours \
on duty.{support}

As part of their duties volunteers also assist in running the organisation, \
so {firstname} contributed to various aspects of publicity events and our \
training programme.{committee}

All the best,

<img class="sig" title="{coord1}" alt="{coord1}'s signature"
     src="Img/sig1.png">
<img class="sig" title="{coord2}" alt="{coord2}'s signature"
     src="Img/sig2.png">

{coord1} and {coord2}<br>
Coordinators of [Edinburgh Nightline](https://ednightline.com), {year}<br>
[coordinator@ednightline.com](mailto:coordinator@ednightline.com)<br>
"""


for vol in volunteerList("data.csv"):
    firstname = vol["Forename"]
    lastname = vol["Surname"]
    print(f"{firstname} {lastname}...", end=" ")

    # check actually did a shift to receive a graduating certificate
    if(int(vol["Short"]) + int(vol["Long"]) + int(vol["Remote IM"]) == 0):
        print("did no shifts so doesn't get a certificate.")
        continue

    pronoun = volunteerPronoun(vol["3R Name"])
    volLetter = letter.format(
        firstname=firstname,
        lastname=lastname,
        pronoun=pronoun,
        joined=vol["Joined"],
        left=vol["Left"],
        duration=durationString(vol["Joined"], vol["Left"]),
        ongoing=ongoingString(vol["Ongoing"]),
        shifts=shiftsString(vol["Short"], vol["Long"], vol["Remote IM"]),
        hours=shiftHours(vol["Short"], vol["Long"], vol["Remote IM"]),
        support=supportString(vol["Emergency"], vol["Drop-In"], vol["On-Call"],
                              pronoun),
        committee=committeeString(vol["Committee"], pronoun),
        coord1=coord1,
        coord2=coord2,
        today=today,
        year=year
    )

    # write and convert letter to PDF file
    filename = f"Certs/{vol['Forename']}_{vol['Surname']}.pdf"
    md2pdf(
        filename.replace(" ", "_"),
        md_content=volLetter,
        base_url=".",
        css_file_path="style.css"
    )

    print("done!")
