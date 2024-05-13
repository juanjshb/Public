package com.dev.misterj.weather.activities;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.dev.misterj.weather.R;
import com.dev.misterj.weather.utils.Networking;
import com.google.android.material.snackbar.Snackbar;

public class LaunchActivity extends AppCompatActivity {

    View rootView;
    private static final int LOCATION_PERMISSION_REQUEST_CODE = 100;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_launch);

        rootView = findViewById(android.R.id.content);
        /*
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
         */

        getReady();
    }

    private void getReady()
    {
        // Check Internet Connection
        if(new Networking(LaunchActivity.this).checkInternetConnection()) {
            // Check if the permission is already granted
            if (ContextCompat.checkSelfPermission(this,
                    Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                // Permission is not granted, request it
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                        LOCATION_PERMISSION_REQUEST_CODE);
            } else {
                // Permission is already granted, proceed with location access
                startActivity(new Intent(LaunchActivity.this,MainActivity.class));
            }
        }
    }

    @Override
    protected void onStart() {
        super.onStart();
        getReady();

    }

    @Override
    protected void onStop() {
        super.onStop();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == LOCATION_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted, proceed with location access
                startActivity(new Intent(LaunchActivity.this,MainActivity.class));
            } else {
                // Permission denied, handle the case
                Snackbar.make(rootView, getString(R.string.permission_required), Snackbar.LENGTH_LONG)
                        .setAction(getString(R.string.okey), new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                // Optionally, you can add functionality here to handle the "Okay" action
                                getReady();
                            }
                        })
                        .show();
            }
        }
    }
}