// ============================================================
//  Tiger built-in: http (WinINet)
// ============================================================
#include <windows.h>
#include <wininet.h>
#pragma comment(lib, "wininet.lib")

namespace tiger_http {

std::string get(const std::string& url) {
    HINTERNET hInternet = InternetOpenA(
        "TigerHTTP/1.0", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
    if (!hInternet)
        throw std::runtime_error("http.get: InternetOpen failed");

    HINTERNET hUrl = InternetOpenUrlA(
        hInternet, url.c_str(), NULL, 0,
        INTERNET_FLAG_RELOAD | INTERNET_FLAG_NO_CACHE_WRITE, 0);
    if (!hUrl) {
        InternetCloseHandle(hInternet);
        throw std::runtime_error("http.get: InternetOpenUrl failed for: " + url);
    }

    std::string result;
    char buf[4096];
    DWORD bytesRead = 0;
    while (InternetReadFile(hUrl, buf, sizeof(buf) - 1, &bytesRead) && bytesRead > 0) {
        buf[bytesRead] = '\0';
        result += buf;
    }
    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    return result;
}

std::string post(const std::string& url, const std::string& data) {
    HINTERNET hInternet = InternetOpenA(
        "TigerHTTP/1.0", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
    if (!hInternet)
        throw std::runtime_error("http.post: InternetOpen failed");

    HINTERNET hConnect = InternetConnectA(
        hInternet, NULL, INTERNET_DEFAULT_HTTP_PORT,
        NULL, NULL, INTERNET_SERVICE_HTTP, 0, 0);
    if (!hConnect) {
        InternetCloseHandle(hInternet);
        throw std::runtime_error("http.post: InternetConnect failed for: " + url);
    }

    HINTERNET hRequest = HttpOpenRequestA(
        hConnect, "POST", url.c_str(), "HTTP/1.1",
        NULL, NULL, INTERNET_FLAG_RELOAD, 0);
    if (!hRequest) {
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hInternet);
        throw std::runtime_error("http.post: HttpOpenRequest failed for: " + url);
    }

    HttpAddRequestHeadersA(hRequest, "Content-Type: application/x-www-form-urlencoded", -1L, HTTP_ADDREQ_FLAG_ADD);

    BOOL sent = HttpSendRequestA(hRequest, NULL, 0, (LPVOID)data.c_str(), (DWORD)data.size());
    if (!sent) {
        InternetCloseHandle(hRequest);
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hInternet);
        throw std::runtime_error("http.post: HttpSendRequest failed");
    }

    std::string result;
    char buf[4096];
    DWORD bytesRead = 0;
    while (InternetReadFile(hRequest, buf, sizeof(buf) - 1, &bytesRead) && bytesRead > 0) {
        buf[bytesRead] = '\0';
        result += buf;
    }

    InternetCloseHandle(hRequest);
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hInternet);
    return result;
}

std::string get_status(const std::string& url) {
    HINTERNET hInternet = InternetOpenA(
        "TigerHTTP/1.0", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
    if (!hInternet)
        throw std::runtime_error("http.get_status: InternetOpen failed");

    HINTERNET hUrl = InternetOpenUrlA(
        hInternet, url.c_str(), NULL, 0,
        INTERNET_FLAG_RELOAD | INTERNET_FLAG_NO_CACHE_WRITE, 0);
    if (!hUrl) {
        InternetCloseHandle(hInternet);
        return "error";
    }

    DWORD status = 0;
    DWORD size = sizeof(status);
    if (!HttpQueryInfoA(hUrl, HTTP_QUERY_STATUS_CODE | HTTP_QUERY_FLAG_NUMBER, &status, &size, NULL)) {
        status = 200;
    }

    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    return std::to_string(status);
}

} // namespace tiger_http