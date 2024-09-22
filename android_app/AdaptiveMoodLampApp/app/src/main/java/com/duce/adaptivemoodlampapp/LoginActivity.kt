package com.duce.adaptivemoodlampapp

import ApiService
import LoginRequest
import TokenResponse
import android.content.Context
import android.content.SharedPreferences
import android.webkit.WebView
import android.widget.Toast
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.PointerIcon.Companion.Text
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

@Composable
fun LoginScreen() {
    // 1초 후에 표시될 다음 화면 UI
    val context = LocalContext.current
    val username = remember { mutableStateOf("") }
    val password = remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        OutlinedTextField(
            value = username.value,
            onValueChange = { username.value = it },
            label = { Text(stringResource(R.string.id_text)) },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = password.value,
            onValueChange = { password.value = it },
            label = { Text(stringResource(R.string.password_text)) },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation()
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = {
            if (username.value.isEmpty() || password.value.isEmpty()) {
                Toast.makeText(context,
                    context.getString(R.string.input_id_pw_text), Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(context,
                    context.getString(R.string.start_login_text), Toast.LENGTH_SHORT).show()
                    processLogin(username = username.value, password = password.value, context)
            }
        }) {
            Text(stringResource(R.string.login_text))
        }
    }
}

fun processLogin(username:String, password:String, context: Context){
    val retrofit = Retrofit.Builder()
        .baseUrl("http://localhost:8000") // 서버 URL
        //        .baseUrl("http://cciicc.cc:66633") // 서버 URL
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    val apiService = retrofit.create(ApiService::class.java)
    val loginRequest = LoginRequest(username, password)

    apiService.login(loginRequest).enqueue(object : Callback<TokenResponse>
    {
        override fun onResponse(call: Call<TokenResponse>, response: Response<TokenResponse>) {
            if (response.isSuccessful){
                val token = response.body()?.token ?: ""
                saveToken(context, token)
                Toast.makeText(context,"로그인 성공" ,Toast.LENGTH_SHORT).show()
                CurrentScreen.currentScreen = 2
            } else{
                Toast.makeText(context,"로그인 실패" ,Toast.LENGTH_SHORT).show()
            }
        }

        override fun onFailure(p0: Call<TokenResponse>, p1: Throwable) {
            Toast.makeText(context,"네트워크 이슈" ,Toast.LENGTH_SHORT).show()
        }
    })

}


fun saveToken(context: Context, token: String) {
    val sharedPreferences: SharedPreferences = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    val editor = sharedPreferences.edit()
    editor.putString("access_token", token)
    editor.apply()
}

//@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    LoginScreen()
}