# PREGUNTAS FRECUENTES Y CATÁLOGO DE SERVICIOS
## Cybersecurity DR — Centro de Ayuda | Julio 2026

---

## 📋 CATÁLOGO DE SERVICIOS

### 1. SOC Gestionado (Security Operations Center)
Nuestro SOC gestionado ofrece monitoreo de seguridad 24/7/365. Incluye:
- Detección y análisis de amenazas en tiempo real.
- Gestión de alertas y triage automatizado.
- Respuesta a incidentes de nivel 1 y 2.
- Reportes ejecutivos mensuales con métricas de seguridad (MTTD, MTTR).
- Integración con SIEM del cliente o provisión de plataforma propia.
- Cumplimiento con frameworks: NIST CSF, ISO 27001, CIS Controls.

### 2. Auditoría de Seguridad y Pentesting
- Auditoría de configuraciones (cloud, on-premise).
- Pruebas de penetración externas e internas.
- Pentesting de aplicaciones web y móviles (OWASP Top 10).
- Evaluación de ingeniería social.
- Entrega de informe ejecutivo + técnico con roadmap de remediación.

### 3. Consultoría en Recuperación ante Desastres (DR)
- Análisis de Impacto al Negocio (BIA).
- Diseño de estrategias de backup y replicación.
- Definición de RTO/RPO alineados a objetivos de negocio.
- Simulacros de recuperación (DR Drills) y documentación de runbooks.
- Arquitectura de alta disponibilidad en multi-nube (OCI, AWS, Azure).

### 4. Capacitación y Concienciación
- Programas de phishing simulation.
- Workshops de seguridad para desarrolladores (Secure Coding).
- Certificaciones internas: Security Awareness Level 1, 2 y 3.

---

## ❓ PREGUNTAS FRECUENTES

### Sobre Incidentes y Respuesta

**P: ¿Qué medidas de seguridad se deben implementar ante un ataque de ransomware?**
R: Ante un ataque de ransomware, se debe aislar inmediatamente los sistemas afectados para evitar la propagación, notificar al equipo de respuesta a incidentes (CSIRT), iniciar el proceso de recuperación desde copias de seguridad limpias y reportar el incidente a las autoridades según el procedimiento establecido en la Política de Seguridad. Es crucial no pagar el rescate y conservar las evidencias para el análisis forense.

**P: ¿Cuáles son los pasos para reportar un incidente de seguridad?**
R: (1) Notificar de inmediato al CSIRT vía csirt@cybersecuritydr.com o línea de emergencia 24/7. (2) No apagar el equipo afectado a menos que sea necesario para contener el daño; preservar logs y pantallas. (3) Completar el formulario de reporte inicial en el portal de seguridad. (4) Cooperar con el equipo forense durante la investigación. (5) Mantener la confidencialidad del incidente hasta comunicación oficial.

**P: ¿Qué es el RTO y el RPO?**
R: El RTO (Recovery Time Objective) es el tiempo máximo de inactividad permitido para un sistema o proceso después de un desastre. El RPO (Recovery Point Objective) es la pérdida de datos máxima aceptable, medida en tiempo. Ambos se definen en el Análisis de Impacto al Negocio (BIA) y son fundamentales para diseñar estrategias de recuperación ante desastres. Por ejemplo, para servicios críticos de Cybersecurity DR, el RTO es de 1 hora y el RPO de 15 minutos.

### Sobre Servicios y Productos

**P: ¿Qué incluye el servicio de SOC gestionado?**
R: Incluye monitoreo 24/7, detección de amenazas, gestión de alertas, respuesta a incidentes de nivel 1 y 2, reportes ejecutivos mensuales con métricas (MTTD, MTTR), integración con SIEM del cliente o provisión de plataforma propia, y cumplimiento con frameworks NIST CSF, ISO 27001 y CIS Controls.

**P: ¿Cómo puedo solicitar un presupuesto para una auditoría de seguridad?**
R: Para solicitar un presupuesto, puede completar el formulario de contacto en nuestra web o enviar un correo a info@cybersecuritydr.com con una breve descripción de sus necesidades. Nuestro equipo de ventas le responderá en menos de 24 horas con un presupuesto personalizado.

**P: ¿Qué certificaciones tienen los profesionales de Cybersecurity DR?**
R: Nuestro equipo técnico cuenta con certificaciones internacionales como CISSP, CEH (Certified Ethical Hacker), CompTIA Security+, GIAC (GCIH, GCIA), OSCP y certificaciones específicas de proveedores cloud (OCI, AWS, Azure). Además, mantenemos un programa de capacitación continua con al menos 40 horas de entrenamiento anual por colaborador.

### Sobre Políticas y Procedimientos

**P: ¿Cómo se clasifica la información en la organización?**
R: La información se clasifica en cuatro niveles: Público (sin restricciones), Interno (uso exclusivo interno), Confidencial (acceso limitado a roles específicos, requiere cifrado) y Restringido (información crítica, acceso con MFA obligatorio y registro de auditoría). Todo documento debe etiquetarse al momento de su creación.

**P: ¿Qué formatos de archivo se pueden subir para ampliar la base de conocimiento?**
R: El agente inteligente de Cybersecurity DR puede procesar documentos en formato PDF, CSV y DOCX. Se recomienda que los archivos no excedan 50 MB y que el texto esté en formato editable (no imágenes escaneadas sin OCR) para garantizar una indexación óptima.

### Sobre Tecnología y Plataforma

**P: ¿En qué nube se despliega la plataforma de Cybersecurity DR?**
R: Nuestra infraestructura principal está desplegada en Oracle Cloud Infrastructure (OCI) utilizando instancias VM.Standard.E2.1.Micro dentro del nivel Always Free para entornos de desarrollo, y shapes flexibles para producción. También operamos entornos multi-nube en AWS y Azure para redundancia.

**P: ¿Cómo se garantiza la seguridad de los datos en el agente inteligente?**
R: El agente utiliza autenticación JWT con contraseñas hasheadas mediante bcrypt, base de datos vectorial persistente (ChromaDB) para embeddings, historial de chat almacenado en SQLite por usuario, y comunicación mediante HTTPS. Los documentos cargados son procesados localmente y no se envían a terceros salvo la API de Gemini para generación de respuestas.

---

## 📞 CANALES DE SOPORTE

| Canal | Horario | Uso recomendado |
|-------|---------|-----------------|
| Portal de tickets | 24/7 | Seguimiento de incidentes y solicitudes formales. |
| Chat del agente IA | 24/7 | Consultas rápidas sobre políticas, procedimientos y servicios. |
| Correo: soporte@cybersecuritydr.com | 24/7 (respuesta en 4h) | Documentación y escalamientos. |
| Teléfono de emergencias | 24/7 | Incidentes críticos activos (ransomware, brecha de datos). |

---

**Última actualización:** 26/07/2026  
**Responsable:** Equipo de Documentación y Calidad — Cybersecurity DR
