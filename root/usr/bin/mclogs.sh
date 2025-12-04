#!/bin/bash
# LOGSDIR must be defined and contain the path to the logs dir of the minecraft server
# usage: mclogs.sh [day [month [year]]] [to_search1] [to_search2] ... [to_search_n]
#        mclogs.sh [-e to_search1] ... [-e to_search_n] [day [month [year]]]
# will display the logs of the date specified, eventually filtered by the differents search fields provided
# if no number is specified, will show the logs of the current day
# if only one number is specified, the script will search logs for date mm/dd/yyyy where dd will be the number provided, and mm and yyyy are the current month and year 
# if only two numbers are specified, the script will search logs for date mm/dd/yyyy where dd and mm will be respectively the numbers provided
# all the "number" fields can be ranges specified by "i:j" (all integers between i and j included)
# all the "number" fields can be negative, in this case they will be interpreted as relative to the current date (f. e. : -1 for the "day" field if we are the 01/01/2000 will be interpreted as 31/12/1999)
#EXAMPLES :
#mclogs #displays the logs of today
# mclogs 12 12 2012 joined left
# mclogs -e "joined" -e "left" 12 12 2012 #two ways to display the lines from the logs of the 12th of december 2012 where the word "joined" OR the word "left" is written
# mclogs 1:31 12 joined #displays the lines from the logs of all the month of december where the word "joined" appears
year=0
month=0
day=0
regex=false
to_search=""
if [ "$1" = "--help" ]; then
        echo >&2 "usage: $0 [day [month [year]]] [to_search1] [to_search2] ... [to_searchn]"
        exit 1
fi
isInt () {
        if [ -n "$1" ] && [ -z "$(echo "$1" | sed -e "s/-\?[0-9]\+$//")" ]; then
                return 0
        else
                return 1
        fi
}
buffer="$0"
noshift=false
while [ $# -ne 0 ]; do
        arg="$1"
        if [ "$regex" = true ]; then
                to_search="-e ${arg@Q} $to_search"
                regex=false
        elif [ "$arg" = '-e' ]; then
               regex=true
        elif echo "$arg" | grep -q -e "^\-\?[0-9]\+:\-\?[0-9]\+$"; then
                i=$(echo "$arg" | cut -d ":" -f 1)
                j=$(echo "$arg" | cut -d ":" -f 2)
                shift
                noshift=true
                for k in $(seq $i $j); do
                        $buffer $k "$@"
                done
                exit 0
        elif isInt "$arg" && [ "$day" -eq 0 ]; then
                day="$arg"
        elif isInt "$arg" && [ "$month" -eq 0 ]; then
                month="$arg"
        elif isInt "$arg" && [ "$year" -eq 0 ]; then
                year="$arg"
        else
                to_search="-e ${arg@Q} $to_search"
        fi
        buffer="$buffer \"$arg\""
        if [ $noshift = false ]; then
                shift
        else
                noshift=false
        fi
done

if [ "$year" -le 0 ]; then
        year=$(($(date -d "now" +"%Y") + year))
fi
year=$(date -d "1/1/$year" +"%Y")

if [ "$month" -le 0 ]; then
        month=$(($(date -d "now" +"%m") + month))
        year=$((year - (month-1)/12))
        month=$(((month-1) % 12 + 1))
fi
month=$(date -d "$month/1/$year" +"%m")

if [ "$day" -le 0 ]; then
        now_today=$(date -d "now" +"%d")
        day=$(($(date -d "$month/$now_today/$year" +"%s") + day*86400))
        year=$(date -d "@$day" +"%Y")
        month=$(date -d "@$day" +"%m")
        day=$(date -d "@$day" +"%d")

fi
day=$(date -d "$month/$day/$year" +"%d")

if [ -z "$to_search" ]; then
        to_search="-e ''"
fi

cd "$LOGSDIR"
find . -type f -name "$year-$month-$day-*.log.gz" -exec bash -c "zcat \"{}\" | grep $to_search --color=always -H --label=\"{}\" -i" \;
if [ "$day/$month/$year" = $(date -d "now" +"%d/%m/%Y") ]; then
        sh -c "grep latest.log --color=always -H -i $to_search"
fi
