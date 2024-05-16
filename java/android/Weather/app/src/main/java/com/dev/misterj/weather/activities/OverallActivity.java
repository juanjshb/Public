package com.dev.misterj.weather.activities;

import android.content.Intent;
import android.location.Address;
import android.location.Geocoder;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.dev.misterj.weather.R;
import com.dev.misterj.weather.utils.FormatConverter;
import com.dev.misterj.weather.webservices.OpenWeather;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class OverallActivity extends AppCompatActivity implements View.OnClickListener {
    String lat, lng;
    TextView tvOverSunset, tvOverSunrise, tvOverTempStatus, tvOverTemp, tvOverDay, tvOverDate, tvOverState,
            tvHumidity, tvPressure, tvWindDirection, tvWind;

    ImageView imgOverGoBack;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_overall);
        /*
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
         */
        imgOverGoBack = (ImageView) findViewById(R.id.imgOverGoBack);
        tvOverSunset =  (TextView) findViewById(R.id.tvOverSunset);
        tvOverSunrise = (TextView) findViewById(R.id.tvOverSunrise);
        tvOverTempStatus = (TextView) findViewById(R.id.tvOverTempStatus);
        tvOverTemp = (TextView) findViewById(R.id.tvOverTemp);
        tvOverDay = (TextView) findViewById(R.id.tvOverDay);
        tvOverDate = (TextView) findViewById(R.id.tvOverDate);
        tvOverState = (TextView) findViewById(R.id.tvOverState);
        tvHumidity = (TextView) findViewById(R.id.tvHumidity);
        tvPressure = (TextView) findViewById(R.id.tvPressure);
        tvWindDirection = (TextView) findViewById(R.id.tvWindDirection);
        tvWind = (TextView) findViewById(R.id.tvWind);


        imgOverGoBack.setOnClickListener(this);


        if(getIntent() != null)
        {
            lat = getIntent().getStringExtra("lat");
            lng = getIntent().getStringExtra("lng");

            new Thread(new Runnable() {
                @Override
                public void run() {
                    // Perform background task here
                    OpenWeather.WeatherForecast curWeather = new OpenWeather().getWeather( Double.valueOf(lat), Double.valueOf(lng), OpenWeather.UNIT_METRIC );
                    // After getting the result, post it to the main thread
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            // Update the UI with the result
                            String strTemp = Double.toString(curWeather.main.temp) + getString(R.string.degree);
                            String strSunrise = getString(R.string.sunrise) +": "+ new FormatConverter().getTimeFromTimestamp(curWeather.sys.sunrise);
                            String strSunset = getString(R.string.sunset) +": "+ new FormatConverter().getTimeFromTimestamp(curWeather.sys.sunset);
                            String strhumidity =  Integer.toString(curWeather.main.humidity)+"%";
                            String strpressure =  Integer.toString(curWeather.main.pressure)+getString(R.string.pressure_unit);
                            String strWspeed = curWeather.wind.speed +" km/h";
                            String strWdirection = Integer.toString(curWeather.wind.deg) + (char) 0x00B0;

                            tvOverTemp.setText(strTemp);
                            tvOverDay.setText(getCurrentDayOfWeek());
                            tvOverDate.setText(getFormattedDate());
                            tvOverTempStatus.setText(curWeather.weather.get(0).main);
                            tvOverSunrise.setText(strSunrise);
                            tvOverSunset.setText(strSunset);

                            tvHumidity.setText(strhumidity);
                            tvPressure.setText(strpressure);
                            tvWindDirection.setText(strWspeed);
                            tvWind.setText(strWdirection);

                        }
                    });
                }
            }).start();



            Geocoder geocoder = new Geocoder(this);
            try {
                List<Address> addresses = geocoder.getFromLocation(Double.parseDouble(lat), Double.parseDouble(lng), 1);
                if (!addresses.isEmpty()) {
                    Address address = addresses.get(0);
                    String state_country = address.getAdminArea() +", "+ address.getCountryName();
                    tvOverState.setText(state_country);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }



    }

    private String getFormattedDate() {
        // Get current date
        Date currentDate = Calendar.getInstance().getTime();

        // Format date
        SimpleDateFormat dateFormat = new SimpleDateFormat("MMMM d'th', yyyy");
        String formattedDate = dateFormat.format(currentDate);

        // Handle ordinal suffix for the day of the month
        int day = Calendar.getInstance().get(Calendar.DAY_OF_MONTH);
        if (day == 1 || day == 21 || day == 31) {
            formattedDate = formattedDate.replace("th", "st");
        } else if (day == 2 || day == 22) {
            formattedDate = formattedDate.replace("th", "nd");
        } else if (day == 3 || day == 23) {
            formattedDate = formattedDate.replace("th", "rd");
        }

        return formattedDate;
    }

    private String getCurrentDayOfWeek() {
        // Get current date
        Date currentDate = Calendar.getInstance().getTime();

        // Format date to get the day of the week
        SimpleDateFormat dayFormat = new SimpleDateFormat("EEEE", Locale.getDefault());
        return dayFormat.format(currentDate);
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.imgOverGoBack)
        {
            startActivity(new Intent(OverallActivity.this,MainActivity.class));
        }
    }
}