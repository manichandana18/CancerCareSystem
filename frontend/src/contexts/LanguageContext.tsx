import React, { createContext, useContext, useState } from 'react';

export type Language = 'en' | 'hi' | 'es' | 'te';

interface TranslationDict {
    [key: string]: {
        [lang in Language]: string;
    };
}

export const translations: TranslationDict = {
    // ── Navbar ──
    'nav.home': { en: 'Home', hi: 'होम', es: 'Inicio', te: 'హోమ్' },
    'nav.upload': { en: 'Upload X-Ray', hi: 'एक्स-रे अपलोड करें', es: 'Subir rayos X', te: 'ఎక్స్-రే అప్‌లోడ్' },
    'nav.wigs': { en: 'Wigs', hi: 'विग', es: 'Pelucas', te: 'విగ్స్' },
    'nav.donate': { en: 'Donate', hi: 'दान करें', es: 'Donar', te: 'దానం చేయండి' },
    'nav.wellness': { en: 'Wellness', hi: 'कल्याण', es: 'Bienestar', te: 'క్షేమం' },
    'nav.login': { en: 'Login', hi: 'लॉगिन', es: 'Acceso', te: 'లాగిన్' },
    'nav.signup': { en: 'Sign Up', hi: 'साइन अप', es: 'Inscribirse', te: 'సైన్ అప్' },

    // ── Login Page ──
    'login.title': { en: 'Sign In', hi: 'साइन इन करें', es: 'Iniciar sesión', te: 'సైన్ ఇన్' },
    'login.subtitle': { en: 'Access your CancerCare AI account', hi: 'अपने कैंसरकेयर AI खाते तक पहुँचें', es: 'Accede a tu cuenta de CancerCare AI', te: 'మీ ఖాతాను యాక్సెస్ చేయండి' },
    'login.email': { en: 'Email Address', hi: 'ईमेल पता', es: 'Correo electrónico', te: 'ఈమెయిల్ చిరునామా' },
    'login.password': { en: 'Password', hi: 'पासवर्ड', es: 'Contraseña', te: 'పాస్‌వర్డ్' },
    'login.submit': { en: 'Sign In', hi: 'साइन इन करें', es: 'Iniciar sesión', te: 'సైన్ ఇన్' },
    'login.processing': { en: 'Signing in...', hi: 'साइन इन हो रहा है...', es: 'Iniciando sesión...', te: 'సైన్ ఇన్ అవుతోంది...' },
    'login.no_account': { en: "Don't have an account?", hi: 'क्या आपके पास खाता नहीं है?', es: '¿No tienes una cuenta?', te: 'ఖాతా లేదా?' },

    // ── Register Page ──
    'reg.title': { en: 'Create Account', hi: 'खाता बनाएं', es: 'Crear cuenta', te: 'ఖాతాను సృష్టించండి' },
    'reg.name': { en: 'Full Name', hi: 'पूरा नाम', es: 'Nombre completo', te: 'పూర్తి పేరు' },
    'reg.submit': { en: 'Create Account', hi: 'खाता बनाएं', es: 'Crear cuenta', te: 'ఖాతాను సృష్టించండి' },
    'reg.processing': { en: 'Processing...', hi: 'प्रसंस्करण...', es: 'Procesando...', te: 'ప్రాసెస్ అవుతోంది...' },
    'reg.verify_title': { en: 'Verify Email', hi: 'ईमेल सत्यापित करें', es: 'Verificar correo', te: 'ఈమెయిల్ వెరిఫై చేయండి' },
    'reg.enter_code': { en: 'Enter the 6-digit code', hi: '6 अंकों का कोड दर्ज करें', es: 'Ingrese el código de 6 dígitos', te: '6-అంకెల కోడ్‌ను నమోదు చేయండి' },
    'reg.email': { en: 'Email Address', hi: 'ईमेल पता', es: 'Correo electrónico', te: 'ఈమెయిల్ చిరునామా' },
    'reg.phone': { en: 'Phone Number', hi: 'फ़ोन नंबर', es: 'Número de teléfono', te: 'ఫోన్ నంబర్' },
    'reg.age': { en: 'Age', hi: 'आयु', es: 'Edad', te: 'వయస్సు' },
    'reg.gender': { en: 'Gender', hi: 'लिंग', es: 'Género', te: 'లింగం' },
    'reg.male': { en: 'Male', hi: 'पुरुष', es: 'Masculino', te: 'పురుషుడు' },
    'reg.female': { en: 'Female', hi: 'महिला', es: 'Femenino', te: 'స్త్రీ' },
    'reg.other': { en: 'Other', hi: 'अन्य', es: 'Otro', te: 'ఇతర' },
    'reg.have_account': { en: 'Already have an account?', hi: 'क्या आपके पास पहले से एक खाता है?', es: '¿Ya tienes una cuenta?', te: 'ఇప్పటికే ఖాతా ఉందా?' },
    'auth.invalid': { en: 'Invalid email or password', hi: 'गलत ईमेल या पासवर्ड', es: 'Email o contraseña incorrectos', te: 'చెల్లని ఇమెయిల్ లేదా పాస్‌వర్డ్' },
    'auth.locked': { en: 'Account locked after failed attempts', hi: 'विफल प्रयासों के बाद खाता लॉक किया गया', es: 'Cuenta bloqueada después de intentos fallidos', te: 'పలు మార్లు విఫలమైన ప్రయత్నాల తర్వాత ఖాతా లాక్ చేయబడింది' },

    // ── Home Page ──
    'home.hero_title': { en: 'AI-Powered Cancer Detection', hi: 'AI-संचालित कैंसर का पता लगाना', es: 'Detección de cáncer con IA', te: 'AI-ఆధారిత క్యాన్సర్ గుర్తింపు' },
    'home.hero_subtitle': { en: 'Early detection saves lives. Upload your medical scans for instant AI analysis.', hi: 'शीघ्र पहचान जीवन बचाती है। तत्काल AI विश्लेषण के लिए अपने मेडिकल स्कैन अपलोड करें।', es: 'La detección temprana salva vidas. Sube tus escaneos médicos para un análisis con IA.', te: 'ముందస్తు గుర్తింపు ప్రాణాలను కాపాడుతుంది. తక్షణ AI విశ్లేషణ కోసం మీ మెడికల్ స్కాన్‌లను అప్‌లోడ్ చేయండి.' },
    'home.get_started': { en: 'Get Started', hi: 'शुरू करें', es: 'Comenzar', te: 'ప్రారంభించండి' },
    'home.learn_more': { en: 'Learn More', hi: 'और जानें', es: 'Más información', te: 'మరింత తెలుసుకోండి' },
    'home.features_title': { en: 'What We Offer', hi: 'हम क्या प्रदान करते हैं', es: 'Lo que ofrecemos', te: 'మేము ఏమి అందిస్తాము' },
    'home.feature_detection': { en: 'Cancer Detection', hi: 'कैंसर का पता लगाना', es: 'Detección de cáncer', te: 'క్యాన్సర్ గుర్తింపు' },
    'home.feature_detection_desc': { en: 'AI-powered analysis of medical scans for early cancer detection', hi: 'शीघ्र कैंसर पहचान के लिए मेडिकल स्कैन का AI विश्लेषण', es: 'Análisis de escaneos médicos con IA para la detección temprana', te: 'ముందస్తు క్యాన్సర్ గుర్తింపు కోసం AI విశ్లేషణ' },
    'home.feature_wellness': { en: 'Wellness Programs', hi: 'कल्याण कार्यक्रम', es: 'Programas de bienestar', te: 'వెల్‌నెస్ కార్యక్రమాలు' },
    'home.feature_wellness_desc': { en: 'Guided exercises and meditation for healing and recovery', hi: 'उपचार और पुनर्प्राप्ति के लिए निर्देशित व्यायाम और ध्यान', es: 'Ejercicios guiados y meditación para la curación', te: 'నయం మరియు రికవరీ కోసం వ్యాయామాలు మరియు ధ్యానం' },
    'home.feature_community': { en: 'Community Support', hi: 'सामुदायिक सहायता', es: 'Apoyo comunitario', te: 'సంఘ సహాయం' },
    'home.feature_community_desc': { en: 'Connect with others, donate wigs, and support patients', hi: 'दूसरों से जुड़ें, विग दान करें, और रोगियों की मदद करें', es: 'Conecta, dona pelucas y apoya a los pacientes', te: 'ఇతరులతో అనుసంధానం, విగ్ దానం, మరియు రోగులకు సహాయం' },
    'home.feature_staging': { en: 'Cancer Staging', hi: 'कैंसर स्टेजिंग', es: 'Estadificación del cáncer', te: 'క్యాన్సర్ స్టేజింగ్' },
    'home.feature_staging_desc': { en: 'AI-estimated cancer staging with personalized recommendations', hi: 'व्यक्तिगत सिफारिशों के साथ AI-अनुमानित कैंसर स्टेजिंग', es: 'Estadificación estimada por IA con recomendaciones', te: 'వ్యక్తిగత సిఫారసులతో AI-అంచనా క్యాన్సర్ స్టేజింగ్' },
    'home.impact_title': { en: 'Our Impact', hi: 'हमारा प्रभाव', es: 'Nuestro impacto', te: 'మా ప్రభావం' },
    'home.scans_analyzed': { en: 'Scans Analyzed', hi: 'स्कैन विश्लेषित', es: 'Escaneos analizados', te: 'స్కాన్‌లు విశ్లేషించబడ్డాయి' },
    'home.accuracy': { en: 'Accuracy Rate', hi: 'सटीकता दर', es: 'Tasa de precisión', te: 'ఖచ్చితత్వ రేటు' },
    'home.patients_helped': { en: 'Patients Helped', hi: 'रोगियों की मदद', es: 'Pacientes ayudados', te: 'రోగులకు సహాయం' },
    'home.trusted_by': { en: 'Trusted by Doctors', hi: 'डॉक्टरों द्वारा विश्वसनीय', es: 'Confianza de los médicos', te: 'వైద్యులచే విశ్వసనీయం' },

    // ── Upload Page ──
    'upload.title': { en: 'Upload Medical Scan', hi: 'मेडिकल स्कैन अपलोड करें', es: 'Subir escaneo médico', te: 'మెడికల్ స్కాన్ అప్‌లోడ్ చేయండి' },
    'upload.subtitle': { en: 'Upload your X-ray or scan for AI analysis', hi: 'AI विश्लेषण के लिए अपना एक्स-रे या स्कैन अपलोड करें', es: 'Sube tu radiografía para análisis con IA', te: 'AI విశ్లేషణ కోసం మీ ఎక్స్‌రే లేదా స్కాన్ అప్‌లోడ్ చేయండి' },
    'upload.drag_drop': { en: 'Drag & Drop or Click to Upload', hi: 'खींचें और छोड़ें या अपलोड करने के लिए क्लिक करें', es: 'Arrastra y suelta o haz clic para subir', te: 'లాగి వదలండి లేదా అప్‌లోడ్ చేయడానికి క్లిక్ చేయండి' },
    'upload.supported': { en: 'Supported formats: JPG, PNG, DICOM', hi: 'समर्थित प्रारूप: JPG, PNG, DICOM', es: 'Formatos compatibles: JPG, PNG, DICOM', te: 'మద్దతు ఫార్మాట్‌లు: JPG, PNG, DICOM' },
    'upload.select_type': { en: 'Select Cancer Type', hi: 'कैंसर प्रकार चुनें', es: 'Selecciona tipo de cáncer', te: 'క్యాన్సర్ రకాన్ని ఎంచుకోండి' },
    'upload.bone': { en: 'Bone Cancer', hi: 'हड्डी का कैंसर', es: 'Cáncer de hueso', te: 'ఎముక క్యాన్సర్' },
    'upload.lung': { en: 'Lung Cancer', hi: 'फेफड़ों का कैंसर', es: 'Cáncer de pulmón', te: 'ఊపిరితిత్తుల క్యాన్సర్' },
    'upload.blood': { en: 'Blood Cancer', hi: 'ब्लड कैंसर', es: 'Cáncer de sangre', te: 'రక్త క్యాన్సర్' },
    'upload.brain': { en: 'Brain Cancer', hi: 'ब्रेन कैंसर', es: 'Cáncer de cerebro', te: 'మెదడు క్యాన్సర్' },
    'upload.skin': { en: 'Skin Cancer', hi: 'त्वचा का कैंसर', es: 'Cáncer de piel', te: 'చర్మ క్యాన్సర్' },
    'upload.breast': { en: 'Breast Cancer', hi: 'स्तन कैंसर', es: 'Cáncer de mama', te: 'రొమ్ము క్యాన్సర్' },
    'upload.analyze': { en: 'Analyze Scan', hi: 'स्कैन का विश्लेषण करें', es: 'Analizar escaneo', te: 'స్కాన్ విశ్లేషించండి' },
    'upload.analyzing': { en: 'Analyzing...', hi: 'विश्लेषण हो रहा है...', es: 'Analizando...', te: 'విశ్లేషిస్తోంది...' },

    // ── Profile Page ──
    'profile.edit_profile': { en: 'Edit Profile', hi: 'प्रोफ़ाइल संपादित करें', es: 'Editar perfil', te: 'ప్రొఫైల్‌ను సవరించండి' },
    'profile.cancel': { en: 'Cancel', hi: 'रद्द करें', es: 'Cancelar', te: 'రద్దు చేయి' },
    'profile.security': { en: 'Security', hi: 'सुरक्षा', es: 'Seguridad', te: 'భద్రత' },
    'profile.verified': { en: 'Verified', hi: 'सत्यापित', es: 'Verificado', te: 'ధృవీకరించబడింది' },
    'profile.access_level': { en: 'Level Access', hi: 'स्तर पहुँच', es: 'Acceso de nivel', te: 'స్థాయి యాక్సెస్' },
    'profile.full_name': { en: 'Full Name', hi: 'पूरा नाम', es: 'Nombre completo', te: 'పూర్తి పేరు' },
    'profile.phone_number': { en: 'Phone Number', hi: 'फ़ोन नंबर', es: 'Número de teléfono', te: 'ఫోన్ నంబర్' },
    'profile.age': { en: 'Age', hi: 'आयु', es: 'Edad', te: 'వయస్సు' },
    'profile.gender': { en: 'Gender', hi: 'लिंग', es: 'Género', te: 'లింగం' },
    'profile.saving': { en: 'Saving...', hi: 'सहेज रहा है...', es: 'Guardando...', te: 'సేవ్ అవుతోంది...' },
    'profile.save_changes': { en: 'Save Changes', hi: 'बदलाव सहेजें', es: 'Guardar cambios', te: 'మార్పులను సేవ్ చేయి' },
    'profile.confidential_info': { en: 'Confidential Info', hi: 'गोपनीय जानकारी', es: 'Información confidencial', te: 'గోప్యమైన సమాచారం' },
    'profile.verified_email': { en: 'Verified Email', hi: 'सत्यापित ईमेल', es: 'Email verificado', te: 'ధృవీకరించబడిన ఇమెయిల్' },
    'profile.secure_phone': { en: 'Secure Phone', hi: 'सुरक्षित फ़ोन', es: 'Teléfono seguro', te: 'సురక్షిత ఫోన్' },
    'profile.account_activity': { en: 'Account Activity', hi: 'खाता गतिविधि', es: 'Actividad de la cuenta', te: 'ఖాతా కార్యాచరణ' },
    'profile.member_since': { en: 'Member Since', hi: 'सदस्यता तिथि', es: 'Miembro desde', te: 'సభ్యత్వం పొందినప్పటి నుండి' },
    'profile.session_status': { en: 'Session Status', hi: 'सत्र की स्थिति', es: 'Estado de la sesión', te: 'సెషన్ స్థితి' },
    'profile.active_session': { en: 'Active Session', hi: 'सक्रिय सत्र', es: 'Sesión activa', te: 'క్రియాశీల సెషన్' },
    'profile.just_created': { en: 'Just created', hi: 'अभी बनाया गया', es: 'Recién creado', te: 'ఇప్పుడే సృష్టించబడింది' },
    'profile.security_level': { en: 'Security Level', hi: 'सुरक्षा स्तर', es: 'Nivel de seguridad', te: 'భద్రతా స్థాయి' },
    'profile.scans_done': { en: 'Scans Done', hi: 'किए गए स्कैन', es: 'Escaneos realizados', te: 'పూర్తయిన స్కాన్‌లు' },
    'profile.reports': { en: 'Reports', hi: 'रिपोर्ट', es: 'Informes', te: 'నివేదికలు' },
    'profile.wellness_score': { en: 'Wellness Score', hi: 'वेलनेस स्कोर', es: 'Puntaje de bienestar', te: 'వెల్‌నెస్ స్కోర్' },
    'profile.trust_level': { en: 'Trust Level', hi: 'विश्वास स्तर', es: 'Nivel de confianza', te: 'నమ్మక స్థాయి' },
    'profile.hipaa_title': { en: 'HIPAA Confidentiality Notice', hi: 'HIPAA गोपनीयता सूचना', es: 'Aviso de confidencialidad HIPAA', te: 'HIPAA గోప్యతా నోటీసు' },
    'profile.hipaa_text': { en: 'Your medical data is protected under HIPAA standards. Only authorized personnel can access your full medical history. Always ensure you are on a secure connection when viewing this page.', hi: 'आपका चिकित्सा डेटा HIPAA मानकों के तहत सुरक्षित है। केवल अधिकृत कर्मचारी आपके पूर्ण चिकित्सा इतिहास तक पहुँच सकते हैं।', es: 'Sus datos médicos están protegidos bajo HIPAA. Solo personal autorizado puede acceder a su historial médico completo.', te: 'మీ వైద్య డేటా HIPAA ప్రమాణాల ప్రకారం రక్షించబడింది. మీ పూర్తి వైద్య చరిత్రను అనుమతించబడిన సిబ్బంది మాత్రమే యాక్సెస్ చేయగలరు.' },
    'profile.change_password': { en: 'Change Password', hi: 'पासवर्ड बदलें', es: 'Cambiar contraseña', te: 'పాస్‌వర్డ్ మార్చు' },
    'profile.current_password': { en: 'Current Password', hi: 'वर्तमान पासवर्ड', es: 'Contraseña actual', te: 'ప్రస్తుత పాస్‌వర్డ్' },
    'profile.new_password': { en: 'New Password', hi: 'नया पासवर्ड', es: 'Nueva contraseña', te: 'కొత్త పాస్‌వర్డ్' },
    'profile.confirm_password': { en: 'Confirm New Password', hi: 'नए पासवर्ड की पुष्टि करें', es: 'Confirmar nueva contraseña', te: 'కొత్త పాస్‌వర్డ్‌ను ధృవీకరించండి' },
    'profile.changing': { en: 'Changing...', hi: 'बदल रहा है...', es: 'Cambiando...', te: 'మారుతోంది...' },
    'profile.update_success': { en: 'Profile updated successfully!', hi: 'प्रोफ़ाइल सफलतापूर्वक अपडेट की गई!', es: '¡Perfil actualizado con éxito!', te: 'ప్రొఫైల్ విజయవంతంగా నవీకరించబడింది!' },
    'profile.update_failed': { en: 'Update failed', hi: 'अपडेट विफल रहा', es: 'Actualización fallida', te: 'నవీకరణ విఫలమైంది' },
    'profile.pw_min_length': { en: 'Password must be at least 6 characters', hi: 'पासवर्ड कम से कम 6 अक्षरों का होना चाहिए', es: 'La contraseña debe tener al menos 6 caracteres', te: 'పాస్‌వర్డ్ కనీసం 6 అక్షరాలు ఉండాలి' },
    'profile.pw_mismatch': { en: 'New passwords do not match', hi: 'नए पासवर्ड मेल नहीं खाते', es: 'Las nuevas contraseñas no coinciden', te: 'కొత్త పాస్‌వర్డ్‌లు సరిపోలడం లేదు' },
    'profile.pw_success': { en: 'Password changed successfully!', hi: 'पासवर्ड सफलतापूर्वक बदल गया!', es: '¡Contraseña cambiada con éxito!', te: 'పాస్‌వర్డ్ విజయవంతంగా మార్చబడింది!' },
    'profile.gender.prefer_not_to_say': { en: 'Prefer not to say', hi: 'बताना नहीं चाहते', es: 'Prefiero no decirlo', te: 'చెప్పడానికి ఇష్టపడలేదు' },
    'profile.select': { en: 'Select', hi: 'चुनें', es: 'Seleccionar', te: 'ఎంచుకోండి' },
    'profile.not_provided': { en: 'Not provided', hi: 'प्रदान नहीं किया गया', es: 'No proporcionado', te: 'అందించబడలేదు' },
    'profile.years': { en: 'years', hi: 'वर्ष', es: 'años', te: 'సంవత్సరాలు' },

    // ── Donation Page ──
    'donate.title': { en: 'Support Cancer Patients', hi: 'कैंसर रोगियों की मदद करें', es: 'Apoya a pacientes con cáncer', te: 'క్యాన్సర్ రోగులకు సహాయం చేయండి' },
    'donate.subtitle': { en: 'Your donation helps fund treatment, research, and support for patients', hi: 'आपका दान उपचार, शोध और रोगी सहायता में मदद करता है', es: 'Tu donación ayuda a financiar tratamiento e investigación', te: 'మీ దానం చికిత్స, పరిశోధన మరియు రోగి సహాయానికి సహాయపడుతుంది' },
    'donate.monetary': { en: 'Monetary Donation', hi: 'मौद्रिक दान', es: 'Donación monetaria', te: 'ద్రవ్య దానం' },
    'donate.wig_donation': { en: 'Wig Donation', hi: 'विग दान', es: 'Donación de peluca', te: 'విగ్ దానం' },
    'donate.amount': { en: 'Donation Amount', hi: 'दान राशि', es: 'Monto de donación', te: 'దాన మొత్తం' },
    'donate.currency': { en: 'Currency', hi: 'मुद्रा', es: 'Moneda', te: 'కరెన్సీ' },
    'donate.payment_method': { en: 'Payment Method', hi: 'भुगतान विधि', es: 'Método de pago', te: 'చెల్లింపు పద్ధతి' },
    'donate.donor_name': { en: 'Your Name', hi: 'आपका नाम', es: 'Tu nombre', te: 'మీ పేరు' },
    'donate.donor_email': { en: 'Email Address', hi: 'ईमेल पता', es: 'Correo electrónico', te: 'ఈమెయిల్ చిరునామా' },
    'donate.message': { en: 'Message (Optional)', hi: 'संदेश (वैकल्पिक)', es: 'Mensaje (Opcional)', te: 'సందేశం (ఐచ్ఛికం)' },
    'donate.submit': { en: 'Donate Now', hi: 'अभी दान करें', es: 'Donar ahora', te: 'ఇప్పుడు దానం చేయండి' },
    'donate.processing': { en: 'Processing...', hi: 'प्रसंस्करण...', es: 'Procesando...', te: 'ప్రాసెస్ అవుతోంది...' },
    'donate.total_donated': { en: 'Total Donated', hi: 'कुल दान', es: 'Total donado', te: 'మొత్తం దానం' },
    'donate.total_donors': { en: 'Total Donors', hi: 'कुल दानदाता', es: 'Total de donantes', te: 'మొత్తం దాతలు' },
    'donate.wigs_donated': { en: 'Wigs Donated', hi: 'विग दान किए गए', es: 'Pelucas donadas', te: 'విగ్‌లు దానం చేయబడ్డాయి' },
    'donate.patients_helped': { en: 'Patients Helped', hi: 'रोगियों की मदद', es: 'Pacientes ayudados', te: 'రోగులకు సహాయం' },
    'donate.impact': { en: 'Your Impact', hi: 'आपका प्रभाव', es: 'Tu impacto', te: 'మీ ప్రభావం' },
    'donate.recent': { en: 'Recent Donations', hi: 'हालिया दान', es: 'Donaciones recientes', te: 'ఇటీవలి దానాలు' },
    'donate.anonymous': { en: 'Anonymous', hi: 'गुमनाम', es: 'Anónimo', te: 'అజ్ఞాత' },
    'donate.success': { en: 'Thank you for your donation!', hi: 'आपके दान के लिए धन्यवाद!', es: '¡Gracias por tu donación!', te: 'మీ దానం కోసం ధన్యవాదాలు!' },
    'donate.wig_type': { en: 'Wig Type', hi: 'विग प्रकार', es: 'Tipo de peluca', te: 'విగ్ రకం' },
    'donate.wig_color': { en: 'Wig Color', hi: 'विग रंग', es: 'Color de peluca', te: 'విగ్ రంగు' },
    'donate.wig_condition': { en: 'Condition', hi: 'स्थिति', es: 'Condición', te: 'పరిస్థితి' },
    'donate.new': { en: 'New', hi: 'नया', es: 'Nuevo', te: 'కొత్త' },
    'donate.gently_used': { en: 'Gently Used', hi: 'हल्के से इस्तेमाल किया', es: 'Poco uso', te: 'తక్కువగా వాడినది' },

    'curr.inr': { en: 'Indian Rupee', hi: 'भारतीय रुपया', es: 'Rupia india', te: 'భారతీయ రూపాయి' },
    'curr.usd': { en: 'US Dollar', hi: 'अमेरिकी डॉलर', es: 'Dólar estadounidense', te: 'యుఎస్ డాలర్' },
    'curr.eur': { en: 'Euro', hi: 'यूरो', es: 'Euro', te: 'యూరో' },
    'curr.gbp': { en: 'British Pound', hi: 'ब्रिटिश पाउंड', es: 'Libra esterlina', te: 'బ్రిటిష్ పౌండ్' },
    'curr.aud': { en: 'Australian Dollar', hi: 'ऑस्ट्रेलियाई डॉलर', es: 'Dólar australiano', te: 'ఆస్ట్రేలియన్ డాలర్' },
    'curr.cad': { en: 'Canadian Dollar', hi: 'कनाडाई डॉलर', es: 'Dólar canadiense', te: 'కెనడియన్ డాలర్' },
    'curr.jpy': { en: 'Japanese Yen', hi: 'जापानी येन', es: 'Yen japonés', te: 'జపనీస్ యెన్' },

    'pay.upi.label': { en: 'UPI', hi: 'यूपीआई', es: 'UPI', te: 'యూపీఐ' },
    'pay.upi.desc': { en: 'Google Pay, PhonePe, Paytm', hi: 'गूगल पे, फोनपे, पेटीएम', es: 'Google Pay, PhonePe, Paytm', te: 'గూగుల్ పే, ఫోన్‌పే, పేటీఎం' },
    'pay.card.label': { en: 'Credit / Debit Card', hi: 'क्रेडिट / डेबिट कार्ड', es: 'Tarjeta de crédito / débito', te: 'క్రెడిట్ / డెబిట్ కార్డ్' },
    'pay.card.desc': { en: 'Visa, Mastercard, RuPay', hi: 'वीज़ा, मास्टरकार्ड, रुपे', es: 'Visa, Mastercard, RuPay', te: 'వీసా, మాస్టర్ కార్డ్, రూపే' },
    'pay.netbanking.label': { en: 'Net Banking', hi: 'नेट बैंकिंग', es: 'Banca en línea', te: 'నెట్ బ్యాంकींग' },
    'pay.netbanking.desc': { en: 'All major banks supported', hi: 'सभी प्रमुख बैंक समर्थित', es: 'Todos los bancos principales', te: 'అన్ని ప్రధాన బ్యాంకులు మద్దతు ఇస్తాయి' },
    'pay.wallet.label': { en: 'Digital Wallet', hi: 'डिजिटल वॉलेट', es: 'Billetera digital', te: 'డిజిటల్ వాలెట్' },
    'pay.wallet.desc': { en: 'PayPal, Amazon Pay', hi: 'पेपाल, अमेज़न पे', es: 'PayPal, Amazon Pay', te: 'పేపాల్, అమెజాన్ పే' },
    'pay.crypto.label': { en: 'Crypto', hi: 'क्रिप्टो', es: 'Cripto', te: 'క్రిప్టో' },
    'pay.crypto.desc': { en: 'Bitcoin, Ethereum', hi: 'बिटकॉइन, एथेरियम', es: 'Bitcoin, Ethereum', te: 'బిట్‌కాయిన్, ఎథెరియం' },

    // ── Wellness Page ──
    'wellness.title': { en: 'Sanctuary of Healing', hi: 'हीलिंग का अभयारण्य', es: 'Santuario de sanación', te: 'హీలింగ్ శాంక్చురీ' },
    'wellness.subtitle': { en: 'Curated wellness rituals designed to support your body and soul through every step of recovery.', hi: 'रिकवरी के हर कदम पर आपके शरीर और आत्मा का समर्थन करने के लिए तैयार किए गए स्वास्थ्य अनुष्ठान।', es: 'Rituales de bienestar diseñados para apoyar su cuerpo y alma.', te: 'రికవరీ యొక్క ప్రతి అడుగులో మీ శరీరం మరియు ఆత్మకు మద్దతు ఇవ్వడానికి రూపొందించబడిన వెల్నెస్ ఆచారాలు.' },
    'wellness.stats.consistency': { en: 'Consistency', hi: 'निरंतरता', es: 'Consistencia', te: 'స్థిరత్వం' },
    'wellness.stats.total_healing': { en: 'Total Healing', hi: 'कुल हीलिंग', es: 'Sanación total', te: 'మొత్తం హీలింగ్' },
    'wellness.all_disciplines': { en: 'All Disciplines', hi: 'सभी अनुशासन', es: 'Todas las disciplinas', te: 'అన్ని విభాగాలు' },
    'wellness.cat.mindfulness': { en: 'Mindfulness', hi: 'सजगता', es: 'Atención plena', te: 'మైండ్‌ఫుల్‌నెస్' },
    'wellness.cat.yoga': { en: 'Yoga', hi: 'योग', es: 'Yoga', te: 'యోగా' },
    'wellness.cat.breathing': { en: 'Breathing', hi: 'साँस लेना', es: 'Respiración', te: 'శ్వాసక్రియ' },
    'wellness.cat.meditation': { en: 'Meditation', hi: 'ध्यान', es: 'Meditación', te: 'ధ్యానం' },
    'wellness.cat.relaxation': { en: 'Relaxation', hi: 'विश्राम', es: 'Relajación', te: 'విశ్రాంతి' },
    'wellness.ritual.start': { en: 'Begin Practice', hi: 'अभ्यास शुरू करें', es: 'Comenzar práctica', te: 'సాధన ప్రారంభించండి' },
    'wellness.ritual.pause': { en: 'Pause Flow', hi: 'प्रवाह रोकें', es: 'Pausar flujo', te: 'ప్రవాహాన్ని ఆపండి' },
    'wellness.ritual.end': { en: 'End Session', hi: 'सत्र समाप्त करें', es: 'Finalizar sesión', te: 'సెషన్ ముగించు' },
    'wellness.ritual.breathe_in': { en: 'Breathe In', hi: 'सांस अंदर लें', es: 'Inhalar', te: 'శ్వాస తీసుకోండి' },
    'wellness.ritual.hold': { en: 'Hold Breath', hi: 'सांस रोकें', es: 'Mantener', te: 'శ్వాస ఆపండి' },
    'wellness.ritual.breathe_out': { en: 'Breathe Out', hi: 'सांस छोड़ें', es: 'Exhalar', te: 'శ్వాస వదలండి' },
    'wellness.ritual.expand': { en: 'Expand Lungs', hi: 'फेफड़े फैलाएं', es: 'Expandir pulmones', te: 'ఊపిరితిత్తులను విస్తరించండి' },
    'wellness.ritual.keep_still': { en: 'Keep Still', hi: 'स्थिर रहें', es: 'Mantente quieto', te: 'నిశ్చలంగా ఉండండి' },
    'wellness.ritual.release': { en: 'Release Tension', hi: 'तनाव मुक्त करें', es: 'Liberar tensión', te: 'ఒత్తిడిని విడుదల చేయండి' },
    'wellness.complete.title': { en: 'Transformation Complete!', hi: 'परिवर्तन पूरा हुआ!', es: '¡Transformación completa!', te: 'పరివర్తన పూర్తయింది!' },
    'wellness.complete.btn': { en: 'Continue Your Journey', hi: 'अपनी यात्रा जारी रखें', es: 'Continúa tu viaje', te: 'మీ ప్రయాణాన్ని కొనసాగించండి' },
    'wellness.guidance': { en: 'Guidance Path', hi: 'मार्गदर्शन पथ', es: 'Camino de guía', te: 'మార్గదర్శక మార్గం' },
    'wellness.benefits': { en: 'Healing Benefits', hi: 'हीलिंग के लाभ', es: 'Beneficios de sanación', te: 'హీలింగ్ ప్రయోజనాలు' },
    'wellness.start_ritual': { en: 'START RITUAL', hi: 'अनुष्ठान शुरू करें', es: 'INICIAR RITUAL', te: 'ఆచారాన్ని ప్రారంభించండి' },
    'wellness.all': { en: 'All', hi: 'सभी', es: 'Todos', te: 'అన్నీ' },
    'wellness.min': { en: 'min', hi: 'मिनट', es: 'min', te: 'నిమి' },
    'wellness.difficulty.beginner': { en: 'Beginner', hi: 'शुरुआत', es: 'Principiante', te: 'ప్రారంభకులకు' },
    'wellness.difficulty.intermediate': { en: 'Intermediate', hi: 'मध्यम', es: 'Intermedio', te: 'మధ్యస్థం' },
    'wellness.difficulty.advanced': { en: 'Advanced', hi: 'उन्नत', es: 'Avanzado', te: 'అధునాతన' },

    // ── Exercise Content ──
    'ex.deep_breathing.title': { en: 'Deep Breathing', hi: 'गहरी सांस लेना', es: 'Respiración profunda', te: 'గాఢ శ్వాస' },
    'ex.deep_breathing.desc': { en: 'Controlled deep breathing to reduce anxiety and promote relaxation.', hi: 'चिंता कम करने और विश्राम को बढ़ावा देने के लिए नियंत्रित गहरी सांस लेना।', es: 'Respiración profunda para reducir la ansiedad.', te: 'ఆందోళనను తగ్గించడానికి మరియు ఉపశమనాన్ని ప్రోత్సహించడానికి నియంత్రిత లోతైన శ్వాస.' },

    'ex.gentle_yoga.title': { en: 'Gentle Yoga Flow', hi: 'कोमल योग प्रवाह', es: 'Flujo suave de yoga', te: 'సున్నితమైన యోగా ప్రవాహం' },
    'ex.gentle_yoga.desc': { en: 'A gentle yoga sequence designed for cancer patients. Low-impact poses to improve flexibility.', hi: 'कैंसर रोगियों के लिए डिज़ाइन किया गया एक कोमल योग अनुक्रम।', es: 'Yoga suave diseñado para pacientes con cáncer.', te: 'క్యాన్సర్ రోగుల కోసం రూపొందించబడిన సున్నితమైన యోగా క్రమం.' },

    'ex.body_scan.title': { en: 'Body Scan Meditation', hi: 'बॉडी स्कैन ध्यान', es: 'Meditación de escaneo corporal', te: 'బాడీ స్కాన్ ధ్యానం' },
    'ex.body_scan.desc': { en: 'Focus on releasing tension and promoting healing awareness through your body.', hi: 'तनाव मुक्त करने और शरीर में हीलिंग के प्रति जागरूकता बढ़ाने पर ध्यान दें।', es: 'Enfoque en liberar tensión y promover la sanación.', te: 'తన్యతను విడుదల చేయడం మరియు శరీరం అంతటా హీలింగ్ అవగాహనను పెంపొందించడంపై దృష్టి పెట్టండి.' },

    'ex.muscle_relax.title': { en: 'Progressive Muscle Relaxation', hi: 'प्रगतिशील मांसपेशी विश्राम', es: 'Relajación muscular progresiva', te: 'ప్రోగ్రెసివ్ కండరాల సడలింపు' },
    'ex.muscle_relax.desc': { en: 'Systematically tense and release muscle groups to reduce physical stress.', hi: 'शारीरिक तनाव को कम करने के लिए मांसपेशियों के समूहों को व्यवस्थित रूप से तनाव और ढीला करें।', es: 'Tensa y relaja grupos musculares sistemáticamente.', te: 'శారీరక ఒత్తిడిని తగ్గించడానికి కండరాల సమూహాలను క్రమపద్ధతిలో బిగించి వదులు చేయండి.' },

    'ex.gratitude.title': { en: 'Gratitude Journaling', hi: 'कृतज्ञता जर्नलिंग', es: 'Diario de gratitud', te: 'కృతజ్ఞతా జర్నలింగ్' },
    'ex.gratitude.desc': { en: 'Write down things you are grateful for to shift focus toward positivity.', hi: 'सकारात्मकता की ओर ध्यान केंद्रित करने के लिए उन चीजों को लिखें जिनके लिए आप आभारी हैं।', es: 'Escribe cosas por las que estás agradecido.', te: 'సానుకూలత వైపు దృష్టి మరల్చడానికి మీరు కృతజ్ఞతతో ఉన్న విషయాలను వ్రాసుకోండి.' },

    'ex.chair_yoga.title': { en: 'Chair Yoga for Recovery', hi: 'रिकवरी के लिए चेयर योग', es: 'Yoga en silla para la recuperación', te: 'రికవరీ కోసం చైర్ యోగా' },
    'ex.chair_yoga.desc': { en: 'Accessible yoga poses while seated. Perfect for patients with limited mobility.', hi: 'बैठे हुए भी सुलभ योग मुद्राएं। सीमित गतिशीलता वाले रोगियों के लिए उपयुक्त।', es: 'Yoga accesible mientras está sentado.', te: 'కూర్చున్నప్పుడు చేయగలిగే యోగాసనాలు. పరిమిత కదలికలు ఉన్న రోగులకు సరైనది.' },

    'ex.hold_breathe.title': { en: 'Hold & Breathe Cycle', hi: 'होल्ड और ब्रीद साइकिल', es: 'Ciclo de mantener y respirar', te: 'హోల్డ్ & బ్రీత్ సైకిల్' },
    'ex.hold_breathe.desc': { en: 'Structured breathing cycle involving holds to improve lung capacity.', hi: 'फेफड़ों की क्षमता में सुधार के लिए होल्ड के साथ संरचित श्वास चक्र।', es: 'Ciclo de respiración con pausas para la capacidad pulmonar.', te: 'ఊపిరితిత్తుల సామర్థ్యాన్ని మెరుగుపరచడానికి హోల్డ్‌లతో కూడిన నిర్మాణాత్మక శ్వాస చక్రం.' },

    'ex.bedside_stretch.title': { en: 'Bedside Stretch & Relax', hi: 'बेडसाइड स्ट्रेच और रिलैक्स', es: 'Estiramiento y relax junto a la cama', te: 'బెడ్‌సైడ్ స్ట్రెచ్ & రిలాక్స్' },
    'ex.bedside_stretch.desc': { en: 'Simple stretches while lying down or sitting on the edge of the bed.', hi: 'बिस्तर पर लेटे हुए या बिस्तर के किनारे बैठे हुए किए जाने वाले सरल खिंचाव।', es: 'Estiramientos simples mientras está acostado.', te: 'పడుకున్నప్పుడు లేదా బెడ్ అంచున కూర్చున్నప్పుడు చేయగలిగే సాధారణ సాగతీత వ్యాయామాలు.' },

    'wellness.session.complete_of': { en: 'of', hi: 'में से', es: 'de', te: 'యొక్క' },
    'wellness.session.complete': { en: 'complete', hi: 'पूरा', es: 'completado', te: 'పూర్తయింది' },
    'wellness.ritual.inhale': { en: 'Inhale', hi: 'सांस लें', es: 'Inhala', te: 'పీల్చండి' },
    'wellness.ritual.hold_short': { en: 'Hold', hi: 'रोकें', es: 'Mantén', te: 'ఆపండి' },
    'wellness.ritual.exhale': { en: 'Exhale', hi: 'छोड़ें', es: 'Exhala', te: 'వదలండి' },
    'wellness.mastery': { en: 'Mastery', hi: 'महारत', es: 'Maestría', te: 'నైపుణ్యం' },

    // ── Wig Content ──
    'wig.natural_bob.name': { en: 'Natural Wave Bob', hi: 'नेचुरल वेव बॉब', es: 'Bob de onda natural', te: 'నేచురల్ వేవ్ బాబ్' },
    'wig.natural_bob.desc': { en: 'Beautiful natural wave bob wig, donated for patients undergoing chemotherapy.', hi: 'कीमोथेरेपी से गुजर रहे रोगियों के लिए दान किया गया सुंदर प्राकृतिक लहरदार बॉब विग।', es: 'Hermosa peluca bob de onda natural.', te: 'కీమోథెరపీ చేయించుకుంటున్న రోగుల కోసం దానం చేసిన అందమైన నేచురల్ వేవ్ బాబ్ విగ్.' },

    'wig.long_straight.name': { en: 'Long Straight Classic', hi: 'लॉन्ग स्ट्रेट क्लासिक', es: 'Clásico largo y recto', te: 'లాంగ్ స్ట్రెయిట్ క్లాసిక్' },
    'wig.long_straight.desc': { en: 'Comfortable long straight wig, lightweight and breathable for everyday wear.', hi: 'आरामदायक लंबा सीधा विग, रोज़ पहनने के लिए हल्का और सांस लेने योग्य।', es: 'Peluca larga y recta cómoda.', te: 'రోజూ ధరించడానికి సౌకర్యవంతమైన పొడవైన స్ట్రెయిట్ విగ్, బరువు తక్కువగా ఉంటుంది.' },

    'wig.curly_confidence.name': { en: 'Curly Confidence', hi: 'कर्ली कॉन्फिडेंस', es: 'Confianza rizada', te: 'కర్లీ కాన్ఫిడెన్స్' },
    'wig.curly_confidence.desc': { en: 'Gorgeous curly wig that adds volume and confidence. Subsidized pricing for patients.', hi: 'शानदार घुंघराला विग जो वॉल्यूम और आत्मविश्वास जोड़ता है।', es: 'Magnífica peluca rizada que aporta volumen.', te: 'వాల్యూమ్ మరియు ఆత్మవిశ్వాసాన్ని ఇచ్చే అందమైన కర్లీ విగ్.' },

    'wig.pixie_power.name': { en: 'Pixie Power', hi: 'पिक्सी पावर', es: 'Poder Pixie', te: 'పిక్సీ పవర్' },
    'wig.pixie_power.desc': { en: 'Chic pixie cut wig, professionally cleaned and ready to wear.', hi: 'ठाठ पिक्सी कट विग, पेशेवर रूप से साफ और पहनने के लिए तैयार।', es: 'Elegante peluca de corte pixie.', te: 'స్టైలిష్ పిక్సీ కట్ విగ్, శుభ్రం చేయబడినది మరియు ధరించడానికి సిద్ధంగా ఉంది.' },

    'wig.silver_grace.name': { en: 'Silver Grace', hi: 'सिल्वर ग्रेस', es: 'Gracia de plata', te: 'సిల్వర్ గ్రేస్' },
    'wig.silver_grace.desc': { en: 'Elegant silver wig for a sophisticated, natural look.', hi: 'एक परिष्कृत, प्राकृतिक लुक के लिए सुरुचिपूर्ण चांदी जैसा विగ।', es: 'Elegante peluca plateada.', te: 'సహజమైన లుక్ కోసం సొగసైన సిల్వర్ విగ్.' },

    'wig.headscarf.name': { en: 'Headscarf Collection', hi: 'हेडस्कार्फ कलेक्शन', es: 'Colección de pañuelos', te: 'హెడ్ స్కార్ఫ్ కలెక్షన్' },
    'wig.headscarf.desc': { en: 'Set of 5 beautiful headscarves in assorted colors and patterns.', hi: 'मिश्रित रंगों और पैटर्नों में 5 सुंदर हेडस्कार्फ का सेट।', es: 'Juego de 5 hermosos pañuelos.', te: 'వివిధ రంగులు మరియు నమూనాలలో 5 అందమైన హెడ్ స్కార్ఫ్‌ల సెట్.' },

    // ── Wig Marketplace ──
    'wigs.title': { en: 'Wig Marketplace', hi: 'विग बाज़ार', es: 'Mercado de pelucas', te: 'విగ్ మార్కెట్‌ప్లేస్' },
    'wigs.subtitle': { en: 'Free wigs for cancer patients — donated with love', hi: 'कैंसर रोगियों के लिए मुफ्त विग — प्यार से दान', es: 'Pelucas gratis para pacientes — donadas con amor', te: 'క్యాన్సర్ రోగుల కోసం ఉచిత విగ్‌లు — ప్రేమతో దానం' },
    'wigs.search': { en: 'Search wigs...', hi: 'विग खोजें...', es: 'Buscar pelucas...', te: 'విగ్‌లు వెతకండి...' },
    'wigs.all_types': { en: 'All Types', hi: 'सभी प्रकार', es: 'Todos los tipos', te: 'అన్ని రకాలు' },
    'wigs.request': { en: 'Request This Wig', hi: 'इस विग का अनुरोध करें', es: 'Solicitar esta peluca', te: 'ఈ విగ్ కోరండి' },
    'wigs.request_form': { en: 'Request Form', hi: 'अनुरोध फ़ॉर्म', es: 'Formulario de solicitud', te: 'అభ్యర్థన ఫారం' },
    'wigs.patient_name': { en: 'Patient Name', hi: 'रोगी का नाम', es: 'Nombre del paciente', te: 'రోగి పేరు' },
    'wigs.reason': { en: 'Why do you need this wig?', hi: 'आपको इस विग की आवश्यकता क्यों है?', es: '¿Por qué necesitas esta peluca?', te: 'ఈ విగ్ మీకు ఎందుకు అవసరం?' },
    'wigs.submit_request': { en: 'Submit Request', hi: 'अनुरोध भेजें', es: 'Enviar solicitud', te: 'అభ్యర్థన పంపండి' },
    'wigs.free': { en: 'FREE', hi: 'मुफ्त', es: 'GRATIS', te: 'ఉచితం' },
    'wigs.available': { en: 'Available', hi: 'उपलब्ध', es: 'Disponible', te: 'అందుబాటులో' },
    'wigs.cancel': { en: 'Cancel', hi: 'रद्द करें', es: 'Cancelar', te: 'రద్దు చేయండి' },
    'wigs.synthetic': { en: 'Synthetic', hi: 'सिंथेटिक', es: 'Sintética', te: 'సింథటిక్' },
    'wigs.human_hair': { en: 'Human Hair', hi: 'असली बाल', es: 'Pelo humano', te: 'మానవ వెంట్రుకలు' },
    'wigs.headwear': { en: 'Headwear', hi: 'सिर का पहनावा', es: 'Gorros', te: 'శిరోభూషణం' },
    'wigs.short': { en: 'Short', hi: 'छोटा', es: 'Corto', te: 'చిన్నది' },
    'wigs.medium': { en: 'Medium', hi: 'मध्यम', es: 'Mediano', te: 'మధ్యస్థం' },
    'wigs.long': { en: 'Long', hi: 'लंबा', es: 'Largo', te: 'పొడవైనది' },
    'wigs.search_label': { en: 'Search', hi: 'खोजें', es: 'Buscar', te: 'వెతకండి' },
    'wigs.type_label': { en: 'Type', hi: 'प्रकार', es: 'Tipo', te: 'రకం' },
    'wigs.currency_label': { en: 'Currency', hi: 'मुद्रा', es: 'Moneda', te: 'కరెన్సీ' },
    'wigs.free_only': { en: 'Free only', hi: 'केवल मुफ्त', es: 'Solo gratis', te: 'ఉచితం మాత్రమే' },
    'wigs.no_results': { en: 'No wigs match your filters', hi: 'आपके फ़िल्टर से कोई विग मेल नहीं खाता', es: 'Ninguna peluca coincide con sus filtros', te: 'మీ ఫిల్టర్‌లకు సరిపోయే విగ్‌లు లేవు' },
    'wigs.request_submitted': { en: 'Request Submitted!', hi: 'अनुरोध भेज दिया गया!', es: '¡Solicitud enviada!', te: 'అభ్యర్థన సమర్పించబడింది!' },
    'wigs.request_success_msg': { en: "We'll review your request and get back to you soon. Stay strong!", hi: 'हम आपके अनुरोध की समीक्षा करेंगे और जल्द ही आपसे संपर्क करेंगे। हिम्मत रखें!', es: 'Revisaremos su solicitud y nos pondremos en contacto pronto. ¡Mantente fuerte!', te: 'మేము మీ అభ్యర్థనను సమీక్షించి, త్వరలో మిమ్మల్ని సంప్రదిస్తాము. ధైర్యంగా ఉండండి!' },
    'wigs.browse_more': { en: 'Browse More Wigs', hi: 'और विग देखें', es: 'Ver más pelucas', te: 'మరిన్ని విగ్‌లను చూడండి' },
    'wigs.donate_cta': { en: 'Have a wig to donate? Help a cancer patient feel confident again.', hi: 'क्या आपके पास दान करने के लिए विग है? कैंसर रोगी को फिर से आत्मविश्वास महसूस करने में मदद करें।', es: '¿Tienes una peluca para donar? Ayuda a un paciente a sentirse seguro de nuevo.', te: 'దానం చేయడానికి మీ వద్ద విగ్ ఉందా? క్యాన్సర్ రోగి మళ్లీ ఆత్మవిశ్వాసంతో ఉండటానికి సహాయపడండి.' },
    'wigs.donate_btn': { en: 'Donate a Wig', hi: 'विग दान करें', es: 'Donar una peluca', te: 'విగ్ దానం చేయండి' },
    'wigs.submitting': { en: 'Submitting...', hi: 'भेजा जा रहा है...', es: 'Enviando...', te: 'సమర్పిస్తోంది...' },
    'wigs.length_label': { en: 'Length', hi: 'लंबाई', es: 'Longitud', te: 'పొడవు' },

    // ── Staging Assessment ──
    'staging.title': { en: 'Cancer Staging Assessment', hi: 'कैंसर स्टेजिंग मूल्यांकन', es: 'Evaluación de estadificación del cáncer', te: 'క్యాన్సర్ స్టేజింగ్ అంచనా' },
    'staging.subtitle': { en: 'Get an AI-estimated cancer stage based on your symptoms', hi: 'अपने लक्षणों के आधार पर AI-अनुमानित कैंसर स्टेज प्राप्त करें', es: 'Obtén una estimación de estadio basada en síntomas', te: 'మీ లక్షణాల ఆధారంగా AI-అంచనా క్యాన్సర్ దశ పొందండి' },
    'staging.select_cancer': { en: 'Select Cancer Type', hi: 'कैंसर प्रकार चुनें', es: 'Selecciona tipo de cáncer', te: 'క్యాన్సర్ రకాన్ని ఎంచుకోండి' },
    'staging.tumor_size': { en: 'Tumor Size', hi: 'ट्यूमर का आकार', es: 'Tamaño del tumor', te: 'కణతి పరిమాణం' },
    'staging.lymph_nodes': { en: 'Lymph Nodes Affected', hi: 'प्रभावित लिम्फ नोड्स', es: 'Ganglios linfáticos afectados', te: 'ప్రభావిత శోషరస కణుపులు' },
    'staging.pain_level': { en: 'Pain Level', hi: 'दर्द का स्तर', es: 'Nivel de dolor', te: 'నొప్పి స్థాయి' },
    'staging.duration': { en: 'Duration of Symptoms', hi: 'लक्षणों की अवधि', es: 'Duración de los síntomas', te: 'లక్షణాల వ్యవధి' },
    'staging.metastasis': { en: 'Metastasis (Spread)', hi: 'मेटास्टेसिस (फैलाव)', es: 'Metástasis (propagación)', te: 'మెటాస్టేసిస్ (వ్యాప్తి)' },
    'staging.next': { en: 'Next', hi: 'अगला', es: 'Siguiente', te: 'తదుపరి' },
    'staging.previous': { en: 'Previous', hi: 'पिछला', es: 'Anterior', te: 'మునుపటి' },
    'staging.assess': { en: 'Get Assessment', hi: 'मूल्यांकन प्राप्त करें', es: 'Obtener evaluación', te: 'అంచనా పొందండి' },
    'staging.assessing': { en: 'Analyzing symptoms...', hi: 'लक्षणों का विश्लेषण...', es: 'Analizando síntomas...', te: 'లక్షణాలను విశ్లేషిస్తోంది...' },
    'staging.result': { en: 'Assessment Result', hi: 'मूल्यांकन परिणाम', es: 'Resultado de la evaluación', te: 'అంచనా ఫలితం' },
    'staging.estimated_stage': { en: 'Estimated Stage', hi: 'अनुमानित स्टेज', es: 'Estadio estimado', te: 'అంచనా దశ' },
    'staging.recommendations': { en: 'Recommendations', hi: 'सिफारिशें', es: 'Recomendaciones', te: 'సిఫారసులు' },
    'staging.medical_recs': { en: 'Medical Recommendations', hi: 'चिकित्सा सिफारिशें', es: 'Recomendaciones médicas', te: 'వైద్య సిఫారసులు' },
    'staging.lifestyle_recs': { en: 'Lifestyle Recommendations', hi: 'जीवनशैली सिफारिशें', es: 'Recomendaciones de estilo de vida', te: 'జీవనశైలి సిఫారసులు' },
    'staging.disclaimer': { en: 'This is an AI estimate for educational purposes only. Please consult an oncologist for proper diagnosis.', hi: 'यह केवल शैक्षिक उद्देश्यों के लिए AI अनुमान है। कृपया उचित निदान के लिए ऑन्कोलॉजिस्ट से परामर्श करें।', es: 'Esta es una estimación de IA solo con fines educativos. Consulte a un oncólogo.', te: 'ఇది విద్యా ప్రయోజనాల కోసం మాత్రమే AI అంచనా. దయచేసి సరైన రోగనిర్ణయం కోసం ఆంకాలజిస్ట్‌ను సంప్రదించండి.' },
    'staging.new_assessment': { en: 'New Assessment', hi: 'नया मूल्यांकन', es: 'Nueva evaluación', te: 'కొత్త అంచనా' },
    'staging.yes': { en: 'Yes', hi: 'हाँ', es: 'Sí', te: 'అవును' },
    'staging.no': { en: 'No', hi: 'नहीं', es: 'No', te: 'లేదు' },
    'staging.none': { en: 'None', hi: 'कोई नहीं', es: 'Ninguno', te: 'ఏదీ లేదు' },
    'staging.small': { en: 'Small', hi: 'छोटा', es: 'Pequeño', te: 'చిన్నది' },
    'staging.medium': { en: 'Medium', hi: 'मध्यम', es: 'Mediano', te: 'మధ్యస్థం' },
    'staging.large': { en: 'Large', hi: 'बड़ा', es: 'Grande', te: 'పెద్దది' },
    'staging.very_large': { en: 'Very Large', hi: 'बहुत बड़ा', es: 'Muy grande', te: 'చాలా పెద్దది' },


    // ── Dashboard ──
    'dashboard.title': { en: 'Dashboard', hi: 'डैशबोर्ड', es: 'Panel de control', te: 'డ్యాష్‌బోర్డ్' },
    'dashboard.welcome': { en: 'Welcome back', hi: 'वापस स्वागत है', es: 'Bienvenido de nuevo', te: 'తిరిగి స్వాగతం' },
    'dashboard.recent_scans': { en: 'Recent Scans', hi: 'हालिया स्कैन', es: 'Escaneos recientes', te: 'ఇటీవలి స్కాన్‌లు' },
    'dashboard.no_scans': { en: 'No scans yet. Upload your first scan!', hi: 'अभी तक कोई स्कैन नहीं। अपना पहला स्कैन अपलोड करें!', es: 'Sin escaneos aún. ¡Sube tu primer escaneo!', te: 'ఇంకా స్కాన్‌లు లేవు. మీ మొదటి స్కాన్ అప్‌లోడ్ చేయండి!' },
    'dashboard.view_all': { en: 'View All History', hi: 'सभी इतिहास देखें', es: 'Ver todo el historial', te: 'మొత్తం చరిత్ర చూడండి' },
    'dashboard.upload_scan': { en: 'Upload New Scan', hi: 'नया स्कैन अपलोड करें', es: 'Subir nuevo escaneo', te: 'కొత్త స్కాన్ అప్‌లోడ్ చేయండి' },

    // ── History ──
    'history.title': { en: 'Analysis History', hi: 'विश्लेषण इतिहास', es: 'Historial de análisis', te: 'విశ్లేషణ చరిత్ర' },
    'history.no_records': { en: 'No analysis records found', hi: 'कोई विश्लेषण रिकॉर्ड नहीं मिला', es: 'No se encontraron registros', te: 'విశ్లేషణ రికార్డులు కనుగొనబడలేదు' },
    'history.delete': { en: 'Delete', hi: 'हटाएं', es: 'Eliminar', te: 'తొలగించు' },
    'history.cancer_type': { en: 'Cancer Type', hi: 'कैंसर प्रकार', es: 'Tipo de cáncer', te: 'క్యాన్సర్ రకం' },
    'history.result': { en: 'Result', hi: 'परिणाम', es: 'Resultado', te: 'ఫలితం' },
    'history.date': { en: 'Date', hi: 'तारीख', es: 'Fecha', te: 'తేదీ' },
    'history.confidence': { en: 'Confidence', hi: 'विश्वास', es: 'Confianza', te: 'నమ్మకం' },

    // ── Common ──
    'common.loading': { en: 'Loading...', hi: 'लोड हो रहा है...', es: 'Cargando...', te: 'లోడ్ అవుతోంది...' },
    'common.error': { en: 'Something went wrong', hi: 'कुछ गलत हो गया', es: 'Algo salió mal', te: 'ఏదో తప్పు జరిగింది' },
    'common.success': { en: 'Success!', hi: 'सफल!', es: '¡Éxito!', te: 'విజయం!' },
    'common.submit': { en: 'Submit', hi: 'जमा करें', es: 'Enviar', te: 'సమర్పించండి' },
    'common.back': { en: 'Back', hi: 'वापस', es: 'Atrás', te: 'వెనుకకు' },
    'common.close': { en: 'Close', hi: 'बंद करें', es: 'Cerrar', te: 'మూసివేయి' },
    'common.search': { en: 'Search', hi: 'खोजें', es: 'Buscar', te: 'వెతకండి' },
    'common.filter': { en: 'Filter', hi: 'फ़िल्टर', es: 'Filtrar', te: 'ఫిల్టర్' },
    'common.last_updated': { en: 'Last updated', hi: 'अंतिम अपडेट', es: 'Última actualización', te: 'చివరి నవీకరణ' },
    'common.stay_strong': { en: 'Stay strong 💕', hi: 'हिम्मत रखें 💕', es: 'Mantente fuerte 💕', te: 'ధైర్యంగా ఉండండి 💕' },
    'common.hope_helps': { en: 'Hope this helps! 💕', hi: 'आशा है कि इससे मदद मिलेगी! 💕', es: '¡Espero que esto ayude! 💕', te: 'ఇది సహాయపడుతుందని ఆశిస్తున్నాను! 💕' },
    'wigs.color_placeholder': { en: 'e.g. Dark Brown, Black, Blonde', hi: 'जैसे कि गहरा भूरा, काला, सुनहरा', es: 'p. ej. Marrón oscuro, negro, rubio', te: 'ఉదా. ముదురు గోధుమ రంగు, నలుపు, జుట్టు రంగు' },

    // ── Colors & Conditions ──
    'color.black': { en: 'Black', hi: 'काला', es: 'Negro', te: 'నలుపు' },
    'color.brown': { en: 'Brown', hi: 'भूरा', es: 'Marrón', te: 'గోధుమ రంగు' },
    'color.blonde': { en: 'Blonde', hi: 'सुनहरा', es: 'Rubio', te: 'జుట్టు రంగు' },
    'color.auburn': { en: 'Auburn', hi: 'लाल-भूरा', es: 'Castaño rojizo', te: 'ఎరుపు-గోధుమ' },
    'color.silver': { en: 'Silver', hi: 'चांदी जैसा', es: 'Plateado', te: 'వెండి రంగు' },
    'color.grey': { en: 'Grey', hi: 'स्लेटी', es: 'Gris', te: 'బూడిద రంగు' },
    'color.assorted': { en: 'Assorted', hi: 'विभिन्न', es: 'Surtido', te: 'వివిధ రకాలు' },
    'length.na': { en: 'N/A', hi: 'लागू नहीं', es: 'N/A', te: 'వర్తించదు' },
    'condition.new': { en: 'New', hi: 'नया', es: 'Nuevo', te: 'కొత్తది' },
    'condition.gently_used': { en: 'Gently Used', hi: 'हल्के से इस्तेमाल किया', es: 'Poco uso', te: 'తక్కువగా వాడినది' },

    // ── Staging Details ──
    'staging.step.type': { en: 'Select Type', hi: 'प्रकार चुनें', es: 'Seleccionar tipo', te: 'రకాన్ని ఎంచుకోండి' },
    'staging.step.symptoms': { en: 'Symptoms', hi: 'लक्षण', es: 'Síntomas', te: 'లక్షణాలు' },
    'staging.step.details': { en: 'Details', hi: 'विवरण', es: 'Detalles', te: 'వివరాలు' },
    'staging.step.results': { en: 'Results', hi: 'परिणाम', es: 'Resultados', te: 'ఫలితాలు' },
    'staging.core_symptoms': { en: 'Core Symptoms', hi: 'मुख्य लक्षण', es: 'Síntomas principales', te: 'ప్రధాన లక్షణాలు' },
    'staging.tnm_desc': { en: 'Answer as accurately as possible based on current medical findings.', hi: 'वर्तमान चिकित्सा निष्कर्षों के आधार पर यथासंभव सटीक उत्तर दें।', es: 'Responda con precisión según los hallazgos médicos.', te: 'ప్రస్తుత వైద్య పరిశోధనల ఆధారంగా వీలైనంత ఖచ్చితంగా సమాధానం చెప్పండి.' },
    'staging.lymph_node_involvement': { en: 'Lymph Node Involvement', hi: 'लिम्फ नोड भागीदारी', es: 'Involucramiento de ganglios', te: 'శోషరస కణుపు ప్రమేయం' },
    'staging.metastasis_spread': { en: 'Metastasis (Spread)', hi: 'मेटास्टेसिस (फैलाव)', es: 'Metástasis (propagación)', te: 'మెటాస్టేసిస్ (వ్యాప్తి)' },
    'staging.pain_level_label': { en: 'Pain Level (0-10)', hi: 'दर्द का स्तर (0-10)', es: 'Nivel de dolor (0-10)', te: 'నొప్పి స్థాయి (0-10)' },
    'staging.fatigue_level': { en: 'Fatigue Level', hi: 'थकान का स्तर', es: 'Nivel de fatiga', te: 'అలసట స్థాయి' },
    'staging.duration_label': { en: 'Symptom Duration (months)', hi: 'लक्षणों की अवधि (महीने)', es: 'Duración de síntomas (meses)', te: 'లక్షణాల వ్యవధి (నెలలు)' },
    'staging.prev_treatment': { en: 'Previous Treatment', hi: 'पिछला उपचार', es: 'Tratamiento previo', te: 'మునుపటి చికిత్స' },
    'staging.additional_details': { en: 'Additional Details', hi: 'अतिरिक्त विवरण', es: 'Detalles adicionales', te: 'అదనపు వివరాలు' },
    'staging.skin_changes_label': { en: 'Skin Changes', hi: 'त्वचा में बदलाव', es: 'Cambios en la piel', te: 'చర్మ మార్పులు' },
    'staging.get_assessment': { en: 'Get Assessment', hi: 'मूल्यांकन प्राप्त करें', es: 'Obtener evaluación', te: 'అంచనా పొందండి' },

    // ── Staging Options ──
    'opt.unknown': { en: 'Unknown / Not Applicable', hi: 'अज्ञात / लागू नहीं', es: 'Desconocido', te: 'తెలియదు / వర్తించదు' },
    'opt.none': { en: 'None', hi: 'कोई नहीं', es: 'Ninguno', te: 'ఏదీ లేదు' },
    'opt.small': { en: 'Small (<2 cm)', hi: 'छोटा (<2 सेमी)', es: 'Pequeño (<2 cm)', te: 'చిన్నది (<2 సెం.మీ)' },
    'opt.medium': { en: 'Medium (2-5 cm)', hi: 'मध्यम (2-5 सेमी)', es: 'Mediano (2-5 cm)', te: 'మధ్యస్థం (2-5 సెం.మీ)' },
    'opt.large': { en: 'Large (>5 cm)', hi: 'बड़ा (>5 सेमी)', es: 'Grande (>5 cm)', te: 'పెద్దది (>5 సెం.మీ)' },
    'opt.lymph.none': { en: 'No involvement', hi: 'कोई भागीदारी नहीं', es: 'Sin involucramiento', te: 'ప్రమేయం లేదు' },
    'opt.lymph.nearby': { en: 'Nearby lymph nodes affected', hi: 'पास के लिम्फ नोड्स प्रभावित', es: 'Ganglios cercanos afectados', te: 'సమీప శోషరస కణుపులు ప్రభావితమయ్యాయి' },
    'opt.lymph.distant': { en: 'Distant lymph nodes affected', hi: 'दूर के लिम्फ नोड्स प्रभावित', es: 'Ganglios distantes afectados', te: 'దూరపు శోషరస కణుపులు ప్రభావితమయ్యాయి' },
    'opt.meta.no': { en: 'No metastasis', hi: 'कोई मेटास्टेसिस नहीं', es: 'Sin metástasis', te: 'మెటాస్టేసిస్ లేదు' },
    'opt.meta.suspected': { en: 'Suspected metastasis', hi: 'संदिग्ध मेटास्टेसिस', es: 'Sospecha de metástasis', te: 'మెటాస్టేసిస్ అనుమానం' },
    'opt.meta.confirmed': { en: 'Confirmed metastasis', hi: 'पुष्टि की गई मेटास्टेसिस', es: 'Metástasis confirmada', te: 'ధృవీకరించబడిన మెటాస్టేసిస్' },
    'opt.treatment.none': { en: 'None', hi: 'कोई नहीं', es: 'Ninguno', te: 'ఏదీ లేదు' },
    'opt.treatment.surgery': { en: 'Surgery', hi: 'सर्जरी', es: 'Cirugía', te: 'సర్జరీ' },
    'opt.treatment.chemo': { en: 'Chemotherapy', hi: 'कीमोथेरेपी', es: 'Quimioterapia', te: 'కీమోథెరపీ' },
    'opt.treatment.radiation': { en: 'Radiation', hi: 'विकिरण', es: 'Radiación', te: 'రేడియేషన్' },
    'opt.treatment.combination': { en: 'Combination', hi: 'संयोजन', es: 'Combinación', te: 'కాంబినేషన్' },

    // ── Checkbox Labels ──
    'check.weight_loss': { en: 'Unexplained Weight Loss', hi: 'अस्पष्टीकृत वजन घटना', es: 'Pérdida de peso inexplicable', te: 'కారణం లేని బరువు తగ్గడం' },
    'check.family_history': { en: 'Family History of Cancer', hi: 'कैंसर का पारिवारिक इतिहास', es: 'Historia familiar de cáncer', te: 'క్యాన్సర్ కుటుంబ చరిత్ర' },
    'check.breathing_diff': { en: 'Breathing Difficulty', hi: 'सांस लेने में कठिनाई', es: 'Dificultad para respirar', te: 'శ్వాస తీసుకోవడంలో ఇబ్బంది' },
    'check.coughing_blood': { en: 'Coughing Blood', hi: 'खून की खांसी', es: 'Tos con sangre', te: 'రక్తం పడటం' },
    'check.lump_detected': { en: 'Lump Detected', hi: 'गांठ का पता चला', es: 'Bulto detectado', te: 'గడ్డ పడినట్లు గుర్తించబడింది' },
    'check.bone_pain': { en: 'Persistent Bone Pain', hi: 'लगातार हड्डी में दर्द', es: 'Dolor óseo persistente', te: 'నిరంతర ఎముక నొప్పి' },
    'check.night_sweats': { en: 'Night Sweats', hi: 'रात को पसीना आना', es: 'Sudores nocturnos', te: 'రాత్రి చెమటలు' },
    'check.swollen_lymph': { en: 'Swollen Lymph Nodes', hi: 'सूजे हुए लिम्फ नोड्स', es: 'Ganglios inflamados', te: 'వాపు ఉన్న శోషరస కణుపులు' },
    'check.headaches': { en: 'Persistent Headaches', hi: 'लगातार सिरदर्द', es: 'Dolores de cabeza', te: 'నిరంతర తలనొప్పి' },
    'check.vision_changes': { en: 'Vision Changes', hi: 'दृष्टि में बदलाव', es: 'Cambios en la visión', te: 'దృష్టి మార్పులు' },
    'check.seizures': { en: 'Seizures', hi: 'दौरे', es: 'Convulsiones', te: 'మూర్ఛలు' },

    // ── Staging Skin Options ──
    'opt.skin.color': { en: 'Color Change', hi: 'रंग में बदलाव', es: 'Cambio de color', te: 'రంగు మార్పు' },
    'opt.skin.border': { en: 'Irregular Border', hi: 'अनियमित सीमा', es: 'Borde irregular', te: 'అక్రమ సరిహద్దు' },
    'opt.skin.growing': { en: 'Growing / Spreading', hi: 'बढ़ना / फैलना', es: 'Creciendo', te: 'పెరగడం / వ్యాపించడం' },
    'opt.skin.bleeding': { en: 'Bleeding / Oozing', hi: 'रक्तस्राव / रिसाव', es: 'Sangrado', te: 'రక్తస్రావం / స్రవించడం' },


    // ── Recommendations ──
    'rec.personalized': { en: 'Personalized Recommendations', hi: 'व्यक्तिगत सिफारिशें', es: 'Recomendaciones personalizadas', te: 'వ్యక్తిగత సిఫారసులు' },
    'rec.critical': { en: 'Critical', hi: 'गंभीर', es: 'Crítico', te: 'నిర్ణాయకమైనది' },
    'rec.high': { en: 'High', hi: 'उच्च', es: 'Alto', te: 'ఎక్కువ' },
    'rec.medium': { en: 'Medium', hi: 'मध्यम', es: 'Medio', te: 'మధ్యస్థం' },

    // ── Benchmarks ──
    'analytics.benchmarks.title': { en: 'Comparative Model Performance', hi: 'तुलनात्मक मॉडल प्रदर्शन', es: 'Rendimiento comparativo de modelos', te: 'తులనాత్మక మోడల్ పనితీరు' },
    'analytics.benchmarks.model': { en: 'Model Architecture', hi: 'मॉडल आर्किटेक्चर', es: 'Arquitectura del modelo', te: 'మోడల్ ఆర్కిటెక్చర్' },
    'analytics.benchmarks.accuracy': { en: 'Accuracy Rate', hi: 'सटीकता दर', es: 'Tasa de precisión', te: 'ఖచ్చితత్వ రేటు' },
    'analytics.benchmarks.desc': { en: 'Our ensemble model consistently outperforms individual classifiers, demonstrating its robustness and superior predictive capability.', hi: 'हमारा पहनावा मॉडल लगातार व्यक्तिगत क्लासिफायर से बेहतर प्रदर्शन करता है, जो इसकी मजबूती और बेहतर भविष्य कहनेवाला क्षमता का प्रदर्शन करता है।', es: 'Nuestro modelo de conjunto supera consistentemente a los clasificadores individuales.', te: 'మా సమిష్టి నమూనా వ్యక్తిగత వర్గీకరణల కంటే స్థిరంగా మెరుగ్గా పని చేస్తుంది.' },
    'analytics.benchmarks.ensemble': { en: 'Ensemble Neural Network', hi: 'एन्सेम्बल न्यूरल नेटवर्क', es: 'Red neuronal de conjunto', te: 'సమిష్టి న్యూరల్ నెట్‌వర్క్' },
    'analytics.benchmarks.vit': { en: 'Vision Transformer (ViT)', hi: 'विज़न ट्रांसफार्मर (ViT)', es: 'Transformador de visión', te: 'విజన్ ట్రాన్స్‌ఫార్మర్ (ViT)' },
    'analytics.benchmarks.cnn': { en: 'Deep CNN (ResNet)', hi: 'डीप सीएनएन (ResNet)', es: 'CNN profunda', te: 'డీప్ CNN (ResNet)' },
    'analytics.benchmarks.gnn': { en: 'Graph Neural Network', hi: 'ग्राफ न्यूरल नेटवर्क', es: 'Red neuronal de grafos', te: 'గ్రాఫ్ న్యూరల్ నెట్‌వర్క్' },
    'analytics.title': { en: 'Analytics Dashboard', hi: 'एनालिटिक्स डैशबोर्ड', es: 'Panel de analítica', te: 'అనలిటిక్స్ డ్యాష్‌బోర్డ్' },
    'analytics.subtitle': { en: 'Performance insights and usage statistics', hi: 'प्रदर्शन अंतर्दृष्टि और उपयोग आँकड़े', es: 'Información de rendimiento y estadísticas', te: 'పనితీరు అంతర్దృష్టులు మరియు వినియోగ గణాంకాలు' },
    'analytics.export.title': { en: 'Export Analytics', hi: 'एनालिटिक्स निर्यात करें', es: 'Exportar analítica', te: 'అనలిటిక్స్ ఎగుమతి చేయండి' },
    'analytics.export.btn': { en: 'Export Analytics Data', hi: 'एनालिटिक्स डेटा निर्यात करें', es: 'Exportar datos de analítica', te: 'అనలిటిక్స్ డేటాను ఎగుమతి చేయండి' },

    // ── Methodology ──
    'methodology.title': { en: 'Methodology: Our Approach', hi: 'कार्यप्रणाली: हमारा दृष्टिकोण', es: 'Metodología: Nuestro enfoque', te: 'పద్దతి: మా విధానం' },
    'methodology.subtitle': { en: 'Our method involves a multi-stage approach, integrating data refinement, model training, and ensemble techniques to ensure robust and accurate cancer prediction.', hi: 'हमारी पद्धति में एक बहु-चरणीय दृष्टिकोण शामिल है, जिसमें मजबूत और सटीक कैंसर भविष्यवाणी सुनिश्चित करने के लिए डेटा शोधन, मॉडल प्रशिक्षण और पहनावा तकनीकों को एकीकृत किया गया है।', es: 'Nuestro método implica un enfoque de varias etapas, integrando el refinamiento de datos, el entrenamiento de modelos y las técnicas de conjunto.', te: 'మా పద్ధతి డేటా శుద్ధీకరణ, మోడల్ శిక్షణ మరియు సమిష్టి పద్ధతులను అనుసంధానిస్తూ, ఖచ్చితమైన క్యాన్సర్ అంచనాను నిర్ధారించడానికి బహుళ-దశల విధానాన్ని కలిగి ఉంటుంది.' },
    'methodology.data_prep': { en: 'Data Preparation', hi: 'डेटा तैयारी', es: 'Preparación de datos', te: 'డేటా తయారీ' },
    'methodology.model_training': { en: 'Model Training', hi: 'मॉडल प्रशिक्षण', es: 'Entrenamiento del modelo', te: 'మోడల్ శిక్షణ' },
    'methodology.ensemble': { en: 'Ensemble Techniques', hi: 'एन्सेम्बल तकनीक', es: 'Técnicas de conjunto', te: 'సమిష్టి పద్ధతులు' },
    'methodology.dp.clean': { en: 'Clean and normalize data', hi: 'डेटा को साफ़ और सामान्य करें', es: 'Limpiar y normalizar datos', te: 'డేటాను శుభ్రపరచండి మరియు సాధారణీకరించండి' },
    'methodology.dp.missing': { en: 'Handle missing values', hi: 'लापता मूल्यों को संभालें', es: 'Manejar valores faltantes', te: 'తప్పిపోయిన విలువలను నిర్వహించండి' },
    'methodology.dp.scale': { en: 'Scale features for consistency', hi: 'निरंतरता के लिए विशेषताओं को स्केल करें', es: 'Escalar características', te: 'స్థిరత్వం కోసం ఫీచర్లను స్కేల్ చేయండి' },
    'methodology.mt.lr': { en: 'Logistic Regression', hi: 'लॉजिस्टिक रिग्रेशन', es: 'Regresión logística', te: 'లాజిస్టిక్ రిగ్రెషన్' },
    'methodology.mt.dt': { en: 'Decision Tree', hi: 'डिसीजन ट्री', es: 'Árbol de decisión', te: 'డెసిషన్ ట్రీ' },
    'methodology.mt.rf': { en: 'Random Forest', hi: 'रैंडम फ़ॉरेस्ट', es: 'Bosque aleatorio', te: 'రాండమ్ ఫారెస్ట్' },
    'methodology.mt.svm': { en: 'Support Vector Machine (SVM)', hi: 'सपोर्ट वेक्टर मशीन (SVM)', es: 'Máquina de vectores de soporte (SVM)', te: 'సపోర్ట్ వెక్టర్ మెషిన్ (SVM)' },
    'methodology.en.voting': { en: 'Voting Classifier', hi: 'वोटिंग क्लासिफायर', es: 'Clasificador de votación', te: 'ఓటింగ్ క్లాసిఫైయర్' },
    'methodology.en.bagging': { en: 'Bagging parallel training', hi: 'बैगिंग समानांतर प्रशिक्षण', es: 'Entrenamiento paralelo bagging', te: 'బ్యాగింగ్ సమాంతర శిక్షణ' },
    'methodology.en.boosting': { en: 'Boosting (AdaBoost)', hi: 'बूस्टिंग (AdaBoost)', es: 'Boosting (AdaBoost)', te: 'బూస్టింగ్ (AdaBoost)' },
};

interface LanguageContextType {
    language: Language;
    setLanguage: (lang: Language) => void;
    t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [language, setLangState] = useState<Language>(() => {
        return (localStorage.getItem('app-lang') as Language) || 'en';
    });

    const setLanguage = (lang: Language) => {
        setLangState(lang);
        localStorage.setItem('app-lang', lang);
        window.location.reload();
    };

    const t = (key: string) => {
        return translations[key]?.[language] || key;
    };

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = () => {
    const context = useContext(LanguageContext);
    if (context === undefined) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
};
