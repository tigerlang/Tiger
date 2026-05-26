// ============================================================
// ============================================================
namespace tiger_gui {
void run() {
    MSG msg;
    while (g_running && GetMessageW(&msg, nullptr, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }
}
} 