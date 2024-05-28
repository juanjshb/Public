package com.example.clm.models;

public class TokenModel {
    public String accessToken;
    public String tokenType;
    public int expiresIn;
    public String scope;
    public String jti;

    public TokenModel(String accessToken, String tokenType, int expiresIn, String scope, String jti)
    {
        this.accessToken = accessToken;
        this.tokenType = tokenType;
        this.expiresIn = expiresIn;
        this.scope = scope;
        this.jti = jti;
    }

    public String getAccessToken() {
        return accessToken;
    }
    public int getExpiresIn() {
        return expiresIn;
    }
    public String getJti() {
        return jti;
    }
    public String getScope() {
        return scope;
    }
    public String getTokenType() {
        return tokenType;
    }
    public void setAccessToken(String accessToken) {
        this.accessToken = accessToken;
    }
    public void setExpiresIn(int expiresIn) {
        this.expiresIn = expiresIn;
    }
    public void setJti(String jti) {
        this.jti = jti;
    }
    public void setScope(String scope) {
        this.scope = scope;
    }
    public void setTokenType(String tokenType) {
        this.tokenType = tokenType;
    }
}
