package com.muhammetcakir.yapayzekamobil


import android.Manifest
import android.app.Activity
import android.app.ProgressDialog
import android.content.ActivityNotFoundException
import android.content.ContentValues
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.ImageDecoder
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.provider.Settings
import android.util.Base64.DEFAULT
import android.util.Base64.encodeToString
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.activity.result.ActivityResult
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import coil.load
import coil.transform.CircleCropTransformation
import com.denzcoskun.imageslider.constants.ScaleTypes
import com.denzcoskun.imageslider.models.SlideModel
import com.google.android.material.snackbar.Snackbar
import com.karumi.dexter.Dexter
import com.karumi.dexter.MultiplePermissionsReport
import com.karumi.dexter.PermissionToken
import com.karumi.dexter.listener.PermissionDeniedResponse
import com.karumi.dexter.listener.PermissionGrantedResponse
import com.karumi.dexter.listener.PermissionRequest
import com.karumi.dexter.listener.multi.MultiplePermissionsListener
import com.karumi.dexter.listener.single.PermissionListener
import com.muhammetcakir.yapayzekamobil.databinding.ActivityMainBinding
import id.ionbit.ionalert.IonAlert
import kotlinx.coroutines.GlobalScope

import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import org.json.JSONException
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit
import kotlin.collections.ArrayList


class MainActivity : AppCompatActivity() {
    private lateinit var binding:ActivityMainBinding
    private lateinit var activityResultLauncher: ActivityResultLauncher<Intent>
    private lateinit var permissionLauncher: ActivityResultLauncher<String>
    private var CAMERA_REQUEST_CODE=1
     private val url = "http://192.168.1.114:8000/process_image/"
    var selectedPicture: Uri? = null
    var selectedBitmap: Bitmap? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding=ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        registerLauncher()
        supportActionBar!!.hide()

        binding.takefoto.setOnClickListener {
            cameraChechpermission()
        }
        binding.upload.setOnClickListener {
            FotografaTıklandıgında(binding.root)
        }

        val imageList=ArrayList<SlideModel>()
        imageList.add(SlideModel(R.drawable.balon,"Balon Çiçeği",ScaleTypes.FIT))
        imageList.add(SlideModel(R.drawable.karahindiba,"Karahindiba",ScaleTypes.FIT))
        imageList.add(SlideModel(R.drawable.birdofparadise,"Bird Of Paradise",ScaleTypes.FIT))
        imageList.add(SlideModel(R.drawable.begonvil2,"Begonvil",ScaleTypes.FIT))
        binding.slider.setImageList(imageList)
    }

    private fun cameraChechpermission() {
        Dexter.withContext(this).withPermission(android.Manifest.permission.CAMERA).withListener(
            object : PermissionListener {

                override fun onPermissionGranted(p0: PermissionGrantedResponse?) {
                    camera()
                }

                override fun onPermissionDenied(p0: PermissionDeniedResponse?) {
                    TODO("Not yet implemented")
                }

                override fun onPermissionRationaleShouldBeShown(
                    p0: PermissionRequest?,
                    p1: PermissionToken?
                ) {
                    showRoationalDialogForPermission()
                }
            }
        ).onSameThread().check()

    }

    private fun showRoationalDialogForPermission() {
        AlertDialog.Builder(this).setMessage("Kamera İçin İzin Ver").
                setPositiveButton("Ayarlara Git"){
                    _,_-> try {
                        val intent=Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                        val uri=Uri.fromParts("package",packageName,null)
                        intent.data=uri
                        startActivity(intent)
                    }catch (e:ActivityNotFoundException){
                        e.printStackTrace()
                    }
                }
            .setNegativeButton("İptal"){
                dialog,_->dialog.dismiss()
            }.show()
    }

    private fun camera() {
        val intent=Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        startActivityForResult(intent,CAMERA_REQUEST_CODE)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == CAMERA_REQUEST_CODE && resultCode == Activity.RESULT_OK) {
            val bitmap = data?.extras?.get("data") as Bitmap
            /*binding.foto.load(bitmap) {
                crossfade(true)
                crossfade(1000)
                transformations(CircleCropTransformation())
            }*/
            djangoyaGonder(bitmap)

            val contentResolver = applicationContext.contentResolver
            val timeStamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
            val imageFileName = "IMG_$timeStamp.jpg"
            val contentValues = ContentValues().apply {
                put(MediaStore.Images.Media.DISPLAY_NAME, imageFileName)
                put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
            }

            val imageUri = contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
            val outputStream = imageUri?.let { contentResolver.openOutputStream(it) }
            outputStream?.use {
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, it)
               // Toast.makeText(this, "Fotoğraf galeriye kaydedildi", Toast.LENGTH_SHORT).show()
            }

        }
    }

     private fun djangoyaGonder(bitmap: Bitmap)
     {
         showProgressDialog()
         GlobalScope.launch {
             val client = OkHttpClient.Builder()
                 .connectTimeout(30, TimeUnit.SECONDS) // Bağlantı süresi
                 .readTimeout(30, TimeUnit.SECONDS)    // Okuma süresi
                 .writeTimeout(30, TimeUnit.SECONDS)   // Yazma süresi
                 .build()
             /*val file2 = getRealPathFromURI(selectedPicture.toString())?.let { File(it) }*/
             val byteArrayOutputStream = ByteArrayOutputStream()
             bitmap.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream)
             val byteArray = byteArrayOutputStream.toByteArray()

             val requestBody: RequestBody = MultipartBody.Builder()
                 .setType(MultipartBody.FORM)
                 .addFormDataPart(
                     "image_file",
                     "photo.jpg",
                     RequestBody.create("image/*".toMediaTypeOrNull(), byteArray)
                 )
                 .build()
             val request = Request.Builder()
                 .url(url)
                 .post(requestBody)
                 .build()
             val response = client.newCall(request).execute()
             Log.d("response", response.toString())
             Log.d("responseeeee", response.message.toString())
             val responseData = response.body?.string()
             if (!responseData.isNullOrEmpty()) {
                 try {
                     val jsonResponse = JSONObject(responseData)
                     val predictionsArray = jsonResponse.optJSONArray("predictions")
                     if (predictionsArray != null) {
                         for (i in 0 until predictionsArray.length()) {
                             val prediction = predictionsArray.getJSONObject(i)
                             val Ad = prediction.optString("Ad")
                             val Habitat = prediction.optString("Habitat")
                             val Renk = prediction.optString("Renk")
                             val Genel = prediction.optString("Genel")
                             val yuzde = prediction.optString("Yuzde")
                             val intent = Intent(applicationContext, com.muhammetcakir.yapayzekamobil.Result::class.java)
                             intent.putExtra("Ad", Ad)
                             intent.putExtra("Habitat", Habitat)
                             intent.putExtra("Renk", Renk)
                             intent.putExtra("Genel", Genel)
                             intent.putExtra("yuzde", yuzde.toString())
                             intent.putExtra("photoBitmap", bitmap)
                             startActivity(intent)
                             Log.d("TAG", "Ad: $Ad, yuzde: ${yuzde.toString()},Renk:$Renk,Habitat:$Habitat,Genel:$Genel")
                         }
                     } else {
                         Log.d("TAG", "Boş veya geçersiz yanıt alındı.")
                     }
                 } catch (e: JSONException) {
                     Log.d("TAG", "JSON yanıtı işlenirken bir hata oluştu.")
                 }
             } else {
                 Log.d("TAG", "Yanıt verisi boş.")
             }

         }
     }

    fun getRealPathFromURI(uri: String): String? {
        val contentResolver = applicationContext.contentResolver
        val cursor = contentResolver.query(Uri.parse(uri), null, null, null, null)
        cursor?.use {
            it.moveToFirst()
            val columnIndex = it.getColumnIndex(MediaStore.Images.ImageColumns.DATA)
            if (columnIndex != -1) {
                return it.getString(columnIndex)
            }
        }
        return null
    }
    fun FotografaTıklandıgında(view: View) {

        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.READ_EXTERNAL_STORAGE
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(
                    this,
                    Manifest.permission.READ_EXTERNAL_STORAGE
                )
            ) {
                Snackbar.make(view, "Galeriye girme izni gerekli", Snackbar.LENGTH_INDEFINITE)
                    .setAction("İzin ver",
                        View.OnClickListener {
                            permissionLauncher.launch(Manifest.permission.READ_EXTERNAL_STORAGE)
                        }).show()
            } else {
                permissionLauncher.launch(Manifest.permission.READ_EXTERNAL_STORAGE)
            }
        } else {
            val intentToGallery =
                Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
            activityResultLauncher.launch(intentToGallery)

        }
    }

    fun registerLauncher() {
        activityResultLauncher = registerForActivityResult(
            ActivityResultContracts.StartActivityForResult()
        ) { result ->
            if (result.resultCode == RESULT_OK) {
                val intentFromResult = result.data
                if (intentFromResult != null) {
                    selectedPicture = intentFromResult.data
                    try {
                        if (Build.VERSION.SDK_INT >= 28) {
                            val source = ImageDecoder.createSource(
                                this@MainActivity.contentResolver,
                                selectedPicture!!
                            )
                            selectedBitmap = ImageDecoder.decodeBitmap(source)
                            binding.foto.setImageBitmap(selectedBitmap)
                        } else {
                            selectedBitmap = MediaStore.Images.Media.getBitmap(
                                this@MainActivity.contentResolver,
                                selectedPicture
                            )
                            binding.foto.setImageBitmap(selectedBitmap)
                        }
                    } catch (e: IOException) {
                        e.printStackTrace()
                    }
                }
            }
        }
        permissionLauncher = registerForActivityResult(
            ActivityResultContracts.RequestPermission()
        ) { result ->
            if (result) {
                //permission granted
                val intentToGallery =
                    Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
                activityResultLauncher.launch(intentToGallery)
            } else {
                //permission denied
                Toast.makeText(this@MainActivity, "Permisson needed!", Toast.LENGTH_LONG).show()
            }
        }
    }
    fun showProgressDialog() {
        IonAlert(this, IonAlert.PROGRESS_TYPE)
            .setTitleText("Fotoğraf Gönderiliyor...")

            .show()
    }


}

//GALERİDEN SSEÇERSEN
/*val requestBody: RequestBody = MultipartBody.Builder()
    .setType(MultipartBody.FORM)
    .addFormDataPart("image_file", file2!!.name, RequestBody.create("image/*".toMediaTypeOrNull(), file2))
    .build()*/