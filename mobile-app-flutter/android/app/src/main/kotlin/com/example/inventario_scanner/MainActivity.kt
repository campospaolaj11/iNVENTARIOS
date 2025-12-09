package com.example.inventario_scanner

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import android.media.MediaPlayer
import android.media.RingtoneManager

class MainActivity : FlutterActivity() {
    private val CHANNEL = "inventario_scanner/sound"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "playSuccess" -> {
                    playSystemSound(RingtoneManager.TYPE_NOTIFICATION)
                    result.success(null)
                }
                "playError" -> {
                    playSystemSound(RingtoneManager.TYPE_ALARM)
                    result.success(null)
                }
                "playWarning" -> {
                    playSystemSound(RingtoneManager.TYPE_RINGTONE)
                    result.success(null)
                }
                else -> result.notImplemented()
            }
        }
    }

    private fun playSystemSound(type: Int) {
        try {
            val uri = RingtoneManager.getDefaultUri(type)
            val mediaPlayer = MediaPlayer.create(applicationContext, uri)
            mediaPlayer.setOnCompletionListener { it.release() }
            mediaPlayer.start()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
