import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://127.0.0.1:8000/ultrasonic/1782699299/create?shipType=tanker&shipArea=Lambung%20%28Hull%29"

class TestUltrasonicCreate(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(URL)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def isi_data_valid(self, skip=None):
        skip = skip or []
        d = self.driver

        if "t_origin" not in skip:
            d.find_element(By.ID, "t_origin").send_keys("2")
            time.sleep(1)

        Select(d.find_element(By.ID, "metode_t_min")).select_by_value("rule_90")
        time.sleep(1)

        if "nilai_ketebalan" not in skip:
            d.find_element(By.ID, "nilai_ketebalan").send_keys("2")
            time.sleep(1)

        if "batas_standar" not in skip:
            d.find_element(By.ID, "batas_standar").send_keys("2")
            time.sleep(1)

        if "frekuensi_ut" not in skip:
            d.find_element(By.ID, "frekuensi_ut").send_keys("2")
            time.sleep(1)

        Select(d.find_element(By.ID, "level_pengujian")).select_by_visible_text("B")
        time.sleep(1)
        Select(d.find_element(By.ID, "kelas_area")).select_by_visible_text("B (Non-Kritis)")
        time.sleep(1)

        if "jenis_cacat" not in skip:
            d.find_element(By.ID, "jenis_cacat").send_keys("Korosi")
            time.sleep(1)

        if "kedalaman_cacat" not in skip:
            d.find_element(By.ID, "kedalaman_cacat").send_keys("2")
            time.sleep(1)

        if "panjang_cacat" not in skip:
            d.find_element(By.ID, "panjang_cacat").send_keys("2")
            time.sleep(1)

        Select(d.find_element(By.ID, "tingkat_keparahan")).select_by_visible_text("Sedang")
        time.sleep(1)

        if "catatan_tambahan" not in skip:
            d.find_element(By.ID, "catatan_tambahan").send_keys("Tidak ada")
            time.sleep(1)

        if "amplitudo_gema" not in skip:
            d.find_element(By.ID, "amplitudo_gema").send_keys("2")
            time.sleep(1)

        if "dac_referensi" not in skip:
            d.find_element(By.ID, "dac_referensi").send_keys("2")
            time.sleep(1)

    def klik_simpan(self):
        button = self.driver.find_element(
            By.XPATH, "//button[contains(text(),'Simpan Data')]"
        )
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);", button)
        time.sleep(1)
        button.click()

    # TC01 - Simpan semua data valid
    def test_TC01_simpan_data_valid(self):
        self.isi_data_valid()
        self.klik_simpan()
        time.sleep(2)

        heading = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(heading.text, "Hasil Analisis Ultrasonic Test")

    # TC02 - Ketebalan desain awal kosong
    def test_TC02_t_origin_kosong(self):
        self.isi_data_valid(skip=["t_origin"])
        self.klik_simpan()

        self.assertIn(
            "The t origin field is required.",
            self.driver.page_source
        )

    # TC03 - Nilai ketebalan kosong
    def test_TC03_nilai_ketebalan_kosong(self):
        self.isi_data_valid(skip=["nilai_ketebalan"])
        self.klik_simpan()

        self.assertIn(
            "The nilai ketebalan field is required.",
            self.driver.page_source
        )

    # TC04 - Batas standar kosong
    def test_TC04_batas_standar_kosong(self):
        self.isi_data_valid(skip=["batas_standar"])
        self.klik_simpan()

        self.assertIn(
            "The batas standar field is required.",
            self.driver.page_source
        )

    # TC05 - Frekuensi UT kosong
    def test_TC05_frekuensi_kosong(self):
        self.isi_data_valid(skip=["frekuensi_ut"])
        self.klik_simpan()

        self.assertIn(
            "The frekuensi ut field is required.",
            self.driver.page_source
        )

    # TC06 - Jenis cacat kosong
    def test_TC06_jenis_cacat_kosong(self):
        self.isi_data_valid(skip=["jenis_cacat"])
        self.klik_simpan()

        self.assertIn(
            "The jenis cacat field is required.",
            self.driver.page_source
        )

    # TC07 - Kedalaman cacat kosong
    def test_TC07_kedalaman_cacat_kosong(self):
        self.isi_data_valid(skip=["kedalaman_cacat"])
        self.klik_simpan()

        self.assertIn(
            "The kedalaman cacat field is required.",
            self.driver.page_source
        )

    # TC08 - Panjang cacat kosong
    def test_TC08_panjang_cacat_kosong(self):
        self.isi_data_valid(skip=["panjang_cacat"])
        self.klik_simpan()

        self.assertIn(
            "The panjang cacat field is required.",
            self.driver.page_source
        )

    # TC09 - Amplitudo gema kosong
    def test_TC09_amplitudo_gema_kosong(self):
        self.isi_data_valid(skip=["amplitudo_gema"])
        self.klik_simpan()

        self.assertIn(
            "The amplitudo gema field is required.",
            self.driver.page_source
        )

    # TC10 - DAC referensi kosong
    def test_TC10_dac_referensi_kosong(self):
        self.isi_data_valid(skip=["dac_referensi"])
        self.klik_simpan()

        self.assertIn(
            "The dac referensi field is required.",
            self.driver.page_source
        )

    # TC11 - Catatan tambahan kosong (tidak wajib)
    def test_TC11_catatan_tambahan_kosong(self):
        self.isi_data_valid(skip=["catatan_tambahan"])
        self.klik_simpan()

        self.assertIn(
            "ultrasonic-analysis",
            self.driver.current_url
        )

    # TC12 - Level pengujian valid (pilih opsi A)
    def test_TC12_level_pengujian(self):
        self.isi_data_valid()
        Select(self.driver.find_element(By.ID, "level_pengujian")).select_by_visible_text("A")
        self.klik_simpan()

        self.assertIn(
            "ultrasonic-analysis",
            self.driver.current_url
        )

    # TC13 - Kelas area valid (pilih opsi A)
    def test_TC13_kelas_area(self):
        self.isi_data_valid()
        Select(self.driver.find_element(By.ID, "kelas_area")).select_by_visible_text("A (Kritis/Midship)")
        self.klik_simpan()

        self.assertIn(
            "ultrasonic-analysis",
            self.driver.current_url
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)