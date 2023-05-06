from cffi import FFI


class Textractor:
    def __init__(self) -> None:
        self._ffi = FFI()
        self._ffi.cdef(
            """
        void start(void(*callback)(const wchar_t*, const wchar_t*));
        void attach(DWORD processId);
        void detach(DWORD processId);
        BOOL inserthook(DWORD processId, const wchar_t* command);
        """
        )
        self._dll = self._ffi.dlopen(r"dllx64\Textractor.dll")

    def start(self, cbk):
        self._callback = self._ffi.callback(
            cdecl="void __cdecl(const wchar_t*, const wchar_t*)",
            python_callable=lambda a, b: cbk(self._ffi.string(a), self._ffi.string(b)),
        )

        self._dll.start(self._callback)

    def attach(self, procid: int):
        self._dll.attach(procid)

    def detach(self, procid: int):
        self._dll.detach(procid)

    def inserthook(self, procid: int, command: str) -> bool:
        ret = self._dll.inserthook(procid, self._ffi.new("wchar_t[]", command))
        if ret:
            return True
        return False


if __name__ == "__main__":
    t = Textractor()

    def cbk(a, b):
        print(a, b)

    t.start(cbk)
    import time
    time.sleep(2)
