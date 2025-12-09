package com.inventario.scanner

import android.media.MediaPlayer
import android.content.Context
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.MethodCall

class SoundPlugin(private val context: Context) {
    private var successPlayer: MediaPlayer? = null
    private var errorPlayer: MediaPlayer? = null
    private var warningPlayer: MediaPlayer? = null

    fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "playSuccess" -> {
                playSuccess()
                result.success(null)
            }
            "playError" -> {
                playError()
                result.success(null)
            }
            "playWarning" -> {
                playWarning()
                result.success(null)
            }
            else -> result.notImplemented()
        }
    }

    private fun playSuccess() {
        try {
            // Usar sonido del sistema para éxito
            val resID = context.resources.getIdentifier("success", "raw", context.packageName)
            if (resID != 0) {
                successPlayer = MediaPlayer.create(context, resID)
            } else {
                // Fallback al sonido de notificación del sistema
                successPlayer = MediaPlayer.create(context, android.media.RingtoneManager.getDefaultUri(android.media.RingtoneManager.TYPE_NOTIFICATION))
            }
            successPlayer?.start()
            successPlayer?.setOnCompletionListener { 
                it.release()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun playError() {
        try {
            val resID = context.resources.getIdentifier("error", "raw", context.packageName)
            if (resID != 0) {
                errorPlayer = MediaPlayer.create(context, resID)
            } else {
                // Fallback al sonido de alarma del sistema
                errorPlayer = MediaPlayer.create(context, android.media.RingtoneManager.getDefaultUri(android.media.RingtoneManager.TYPE_ALARM))
            }
            errorPlayer?.start()
            errorPlayer?.setOnCompletionListener { 
                it.release()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun playWarning() {
        try {
            val resID = context.resources.getIdentifier("warning", "raw", context.packageName)
            if (resID != 0) {
                warningPlayer = MediaPlayer.create(context, resID)
            } else {
                // Fallback
                warningPlayer = MediaPlayer.create(context, android.media.RingtoneManager.getDefaultUri(android.media.RingtoneManager.TYPE_RINGTONE))
            }
            warningPlayer?.start()
            warningPlayer?.setOnCompletionListener { 
                it.release()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun dispose() {
        successPlayer?.release()
        errorPlayer?.release()
        warningPlayer?.release()
    }
}
