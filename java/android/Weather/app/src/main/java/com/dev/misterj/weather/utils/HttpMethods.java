package com.dev.misterj.weather.utils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class HttpMethods {

    private static String addParametersToUrl(String baseUrl, HashMap<String, String> parameters) {
        if (parameters != null) {
            StringBuilder urlBuilder = new StringBuilder(baseUrl);

            // Check if URL already contains "?" to determine how to append parameters
            if (baseUrl.contains("?")) {
                urlBuilder.append("&");
            } else {
                urlBuilder.append("?");
            }

            // Iterate through parameters and append to URL
            for (Map.Entry<String, String> entry : parameters.entrySet()) {
                String key = entry.getKey();
                String value = entry.getValue();
                urlBuilder.append(key).append("=").append(value).append("&");
            }

            // Remove the last "&"
            urlBuilder.deleteCharAt(urlBuilder.length() - 1);
            return urlBuilder.toString();
        } else {
            return baseUrl;
        }
    }

    public String GET(String baseUrl, HashMap<String, String> parameters, HashMap<String, String> headers) {
        String link = addParametersToUrl(baseUrl, parameters);
        try {
            URL url = new URL(link);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            if(headers != null)
            {
                for (String key : headers.keySet()) {
                    connection.setRequestProperty(key, headers.get(key));
                }
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String shortUrl = reader.readLine();
            reader.close();

            return shortUrl;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
