import globalPluginHandler
import ui
import scriptHandler
import urllib.request
import re
import threading

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# دالة جلب التاريخ وكشطه من الموقع في الخلفية لضمان عدم تجميد NVDA
	def fetch_hijri_date(self):
		url = "https://dar-alifta.org"
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
		req = urllib.request.Request(url, headers=headers)
		
		try:
			# جلب محتوى HTML الخاص بالصفحة الرئيسية
			html_content = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
			
			# استخدام نفس النمط الناجح للبحث عن التاريخ الهجري
			match = re.search(r'\d+\s+[\u0600-\u06FF\s]+\d+\s*هـ', html_content)
			
			if match:
				clean_date = match.group(0).strip()
				# إزالة أي مسافات مضاعفة زائدة في النص لجعل النطق منساباً
				clean_date = re.sub(r'\s+', ' ', clean_date)
				ui.message(f"التاريخ الهجري اليوم: {clean_date}")
			else:
				ui.message("تعذر استخراج التاريخ الهجري من تصميم الصفحة الحالي.")
				
		except Exception:
			ui.message("عذرًا، فشل الاتصال بموقع دار الإفتاء. تحقق من جودة الإنترنت لديك.")

	# السكريبت الذي ينطلق عند الضغط على الاختصار
	def script_announceHijriDate(self, gesture):
		ui.message("جاري جلب التاريخ من دار الإفتاء...")
		# تشغيل دالة الجلب في Thread منفصل لحماية قارئ الشاشة من التوقف المؤقت
		threading.Thread(target=self.fetch_hijri_date, daemon=True).start()

	# وصف الاختصار في لوحة تحكم NVDA
	script_announceHijriDate.__doc__ = "ينطق التاريخ الهجري الحالي المعتمد من دار الإفتاء المصرية."

	# ربط السكريبت بالاختصار الافتراضي (NVDA + Shift + H)
	__gestures = {
		"kb:NVDA+shift+h": "announceHijriDate",
	}
