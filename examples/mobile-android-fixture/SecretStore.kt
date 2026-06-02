package com.example.vuln

import android.content.Context

class SecretStore(private val ctx: Context) {
    fun storeToken(token: String) {
        val prefs = ctx.getSharedPreferences("auth", Context.MODE_PRIVATE)
        prefs.edit().putString("api_token", token).apply()  // MASVS-STORAGE-1: plaintext token in default prefs
    }

    companion object {
        // MASVS-CRYPTO-2: hard-coded encryption key
        val KEY: ByteArray = "ThisIsASecret123".toByteArray()
    }
}
