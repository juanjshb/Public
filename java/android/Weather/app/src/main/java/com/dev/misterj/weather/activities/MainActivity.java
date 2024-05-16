package com.dev.misterj.weather.activities;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.os.Bundle;
import android.os.Looper;
import android.view.View;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.dev.misterj.weather.R;
import com.dev.misterj.weather.utils.FormatConverter;
import com.dev.misterj.weather.webservices.OpenWeather;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.material.snackbar.Snackbar;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private static final int LOCATION_PERMISSION_REQUEST_CODE = 100;
    private FusedLocationProviderClient fusedLocationClient;
    private LocationRequest locationRequest;
    private LocationCallback locationCallback;
    View rootView;
    private static final Executor executor = Executors.newSingleThreadExecutor();
    TextView tvTemperature, tvTemperatureDegree, tvStateCountry, tvWeatherStatus, tvSunrise, tvSunset,
            tvTempFeels, tvTempMin, tvTempMax, tvSeeOverAll;

    Location lastLocation;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        rootView = findViewById(android.R.id.content);
        /*
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
         */

        ///Prepare Objects
        tvTemperature = (TextView) findViewById(R.id.tvTemperature);
        tvTemperatureDegree = (TextView) findViewById(R.id.tvTemperatureDegree);
        tvWeatherStatus = (TextView) findViewById(R.id.tvWeatherStatus);
        tvStateCountry = (TextView) findViewById(R.id.tvStateCountry);
        tvSunrise = (TextView) findViewById(R.id.tvSunrise);
        tvSunset = (TextView) findViewById(R.id.tvSunset);
        tvSeeOverAll = (TextView) findViewById(R.id.tvSeeOverAll);
        tvTempFeels = (TextView) findViewById(R.id.tvTempFeels);
        tvTempMin = (TextView) findViewById(R.id.tvTempMin);
        tvTempMax = (TextView) findViewById(R.id.tvTempMax);

        tvSeeOverAll.setOnClickListener(this);

        // Initialize fused location client
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this);

        // Create location request
        locationRequest = LocationRequest.create()
                .setInterval(10000) // 10 seconds
                .setFastestInterval(5000) // 5 seconds
                .setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);

        // Create location callback
        locationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(LocationResult locationResult) {
                if (locationResult == null) {
                    return;
                }
                for (Location location : locationResult.getLocations()) {
                    // Handle location updates
                    updateLocationUI(location);
                }
            }
        };
        checkLocationPermission();
    }

    private void checkLocationPermission() {
        // Check if the permission is already granted
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // Permission is not granted, request it
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    LOCATION_PERMISSION_REQUEST_CODE);
        } else {
            // Permission is already granted, proceed with location access
            requestLocationUpdates();
        }
    }

    private void requestLocationUpdates() {
        ///Not required already asked for permissions
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        fusedLocationClient.requestLocationUpdates(locationRequest, locationCallback, Looper.getMainLooper());
    }

    private void updateLocationUI(Location location) {
        // Update UI with the current location
        if (location != null) {

            lastLocation = location;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    // Perform background task here
                    OpenWeather.WeatherForecast curWeather = new OpenWeather().getWeather(location.getLatitude(), location.getLongitude(), OpenWeather.UNIT_METRIC );
                    // After getting the result, post it to the main thread
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            // Update the UI with the result

                            String strTemp = Double.toString(curWeather.main.temp);
                            String strTempFeels = getString(R.string.feels_like) + Double.toString(curWeather.main.feels_like);
                            String strTempMin = getString(R.string.min_temp) + Double.toString(curWeather.main.temp_min);
                            String strTempMax = getString(R.string.max_temp) + Double.toString(curWeather.main.temp_max);
                            String strSunrise = getString(R.string.sunrise) +": "+ new FormatConverter().getTimeFromTimestamp(curWeather.sys.sunrise);
                            String strSunset = getString(R.string.sunset) +": "+ new FormatConverter().getTimeFromTimestamp(curWeather.sys.sunset);

                            tvTemperature.setText(strTemp);
                            tvWeatherStatus.setText(curWeather.weather.get(0).main);
                            tvSunrise.setText(strSunrise);
                            tvSunset.setText(strSunset);
                            tvTempFeels.setText(strTempFeels);
                            tvTempMin.setText(strTempMin);
                            tvTempMax.setText(strTempMax);
                        }
                    });
                }
            }).start();



            Geocoder geocoder = new Geocoder(this);
            try {
                List<Address> addresses = geocoder.getFromLocation(location.getLatitude(), location.getLongitude(), 1);
                if (!addresses.isEmpty()) {
                    Address address = addresses.get(0);
                    String state_country = address.getAdminArea() +", "+ address.getCountryName();
                    tvStateCountry.setText(state_country);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == LOCATION_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted, proceed with location access
                requestLocationUpdates();
            } else {
                // Permission denied, show a toast
                Snackbar.make(rootView, getString(R.string.permission_required), Snackbar.LENGTH_LONG)
                        .setAction(getString(R.string.okey), new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                // Optionally, you can add functionality here to handle the "Okay" action
                                checkLocationPermission();
                            }
                        })
                        .show();
            }
        }
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.tvSeeOverAll)
        {
            if(lastLocation != null)
            {
                Intent a = new Intent(MainActivity.this,OverallActivity.class);
                a.putExtra("lat", Double.toString(lastLocation.getLatitude()));
                a.putExtra("lng", Double.toString(lastLocation.getLongitude()));
                startActivity(a);
            }
        }
    }
}