package com.dev.misterj.weather.webservices;

import com.dev.misterj.weather.utils.HttpMethods;
import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.HashMap;

public class OpenWeather {
    private static final String BASE_URL = "https://api.openweathermap.org/data/2.5/";
    private static final String API_KEY = "34f86bb430813233577758a9fc63e143"; // Replace with your actual API key

    public static String UNIT_METRIC = "metric";
    public static String UNIT_IMPERIAL = "imperial";

    public WeatherForecast getWeather(double latitude, double longitude, String unit) {
        HashMap<String, String> parameters = new HashMap<>();
        parameters.put("appid", API_KEY);
        parameters.put("lat", Double.toString(latitude));
        parameters.put("lon", Double.toString(longitude));
        parameters.put("units", unit);

        Gson gson = new Gson();
        String json = new HttpMethods().GET(BASE_URL + "weather", parameters, null);
        return gson.fromJson(json, WeatherForecast.class);
    }

    public static class Clouds {
        public int all;
    }

    public static class Coord {
        public double lon;
        public double lat;
    }

    public static class Main {
        public double temp;
        public double feels_like;
        public double temp_min;
        public double temp_max;
        public int pressure;
        public int humidity;
    }

    public static class WeatherForecast {
        public Coord coord;
        public ArrayList<Weather> weather;
        public String base;
        public Main main;
        public int visibility;
        public Wind wind;
        public Clouds clouds;
        public int dt;
        public Sys sys;
        public int timezone;
        public int id;
        public String name;
        public int cod;
    }

    public static class Sys {
        public int type;
        public int id;
        public String country;
        public int sunrise;
        public int sunset;
    }

    public static class Weather {
        public int id;
        public String main;
        public String description;
        public String icon;
    }

    public static class Wind {
        public double speed;
        public int deg;
    }
}
