package com.muhammetcakir.yapayzekamobil

import android.content.Intent
import android.graphics.Bitmap
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.core.net.toUri
import com.muhammetcakir.yapayzekamobil.databinding.ActivityResultBinding

class Result : AppCompatActivity() {
    private lateinit var binding: ActivityResultBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding= ActivityResultBinding.inflate(layoutInflater)
        setContentView(binding.root)
        supportActionBar!!.hide()
        val Ad = intent.getStringExtra("Ad")
        val Habitat = intent.getStringExtra("Habitat")
        val Renk = intent.getStringExtra("Renk")
        val Genel = intent.getStringExtra("Genel")
        val yuzde = intent.getStringExtra("yuzde")
        val photoBitmap = intent.getParcelableExtra<Bitmap>("photoBitmap")

        if (Ad!=null || Habitat!=null||Renk!=null||Genel!=null )
        {
            binding.Adi.text=Ad +" "+"(${yuzde})"
            binding.rengi.text=Renk
            binding.habitat.text=Habitat
            binding.Genel.text=Genel
            binding.foto.setImageBitmap(photoBitmap)

        }
        binding.geridon.setOnClickListener {
            startActivity(Intent(this,MainActivity::class.java))
        }


    }


}