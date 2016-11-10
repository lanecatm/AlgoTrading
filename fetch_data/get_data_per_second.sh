startTime=084000
endTime=154000
#Section promgram

echo 'Task schedule Time: ('$startTime') program: ('$program') Waiting...'

while true;
do
    curTime=$(date "+%H%M%S")
    week=`date +%w`
    if [ $week -eq 6 ] || [ $week -eq 0 ];then
        sleep 1
        continue
    else
        if [ "$curTime" -gt "$startTime" ];then
            if [ "$curTime" -lt "$endTime" ];then
                echo 'run'$curTime
                python ./marketDataGetter.py
            fi

        fi
    fi
done
