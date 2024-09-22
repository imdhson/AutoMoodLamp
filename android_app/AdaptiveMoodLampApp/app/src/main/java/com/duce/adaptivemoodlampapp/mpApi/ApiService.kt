import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

data class LoginRequest(val id: String, val password: String)
data class RegisterRequest(val id: String, val password: String)
data class TokenResponse(val token: String)

interface ApiService {
    @POST("/auth/login/")
    fun login(@Body request: LoginRequest): Call<TokenResponse>

    @POST("/auth/register/")
    fun register(@Body request: RegisterRequest): Call<TokenResponse>
}