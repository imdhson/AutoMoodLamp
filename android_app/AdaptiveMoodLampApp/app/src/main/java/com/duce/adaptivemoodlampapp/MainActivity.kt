package com.duce.adaptivemoodlampapp

import BluetoothDeviceList
import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.WebView
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.duce.adaptivemoodlampapp.ui.theme.AdaptiveMoodLampAppTheme
import kotlinx.coroutines.delay

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AdaptiveMoodLampAppTheme {
//                LaunchedEffect(Unit) {
//                    delay(1000)
//                    CurrentScreen.currentScreen = 1
//                }
                CurrentScreen.currentScreen = 1
                ScreenSwitcher(CurrentScreen.currentScreen)
            }
        }
    }
}

@Composable
fun ScreenSwitcher(currentScreen: Int, modifier: Modifier = Modifier) {
    Column {
        AnimatedContent(targetState = currentScreen) { screen ->
            when (screen) {
                0 -> Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    AppName(
                        name = stringResource(R.string.adaptive_mood_lamp),
                        sub = stringResource(R.string.duce_team_name),
                        modifier = Modifier.padding(innerPadding)
                    )
                }

                1 -> LoginScreen()
                2 -> BluetoothDeviceList()
            }
        }
    }
}


@Composable
fun AppName(name: String, sub: String, modifier: Modifier = Modifier) {
    Column(
        modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        CircularProgressIndicator(
            modifier = modifier.size(64.dp),
        )
        Text(
            text = name,
            fontSize = 50.sp,
            lineHeight = 20.sp,
            textAlign = TextAlign.Center,
        )
        Text(
            text = sub,
        )
    }

}


//@Preview(showBackground = true, name="test")
@Composable
fun AppNamePreview() {
    AdaptiveMoodLampAppTheme {
        AppName("적응형 무드램프", "대구대학교 컴퓨터공학과 새로운 팀")
    }
}