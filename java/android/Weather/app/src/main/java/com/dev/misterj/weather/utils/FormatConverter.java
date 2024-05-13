package com.dev.misterj.weather.utils;

import java.text.SimpleDateFormat;
import java.util.Date;

public class FormatConverter {
    public String TimestampToDatetime(long  timestamp)
    {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date date = new Date(timestamp);
        String formattedDate = dateFormat.format(date);
        return formattedDate;
    }

    public String getDateFromTimestamp(long  timestamp)
    {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date date = new Date(timestamp);
        String formattedDate = dateFormat.format(date);
        return formattedDate.split(" ")[0];
    }
    public String getTimeFromTimestamp(long  timestamp)
    {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date date = new Date(timestamp);
        String formattedDate = dateFormat.format(date);
        return formattedDate.split(" ")[1];
    }
}
