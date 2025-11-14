# Historial de Versiones

Con el paso del tiempo el proyecto ha evolucionado en alcance, arquitectura y requerimientos. Debido a que cada versión introdujo cambios significativos en la estructura interna, se decidió mantenerlas documentadas para referencia técnica.

## Versión 1 (Deprecada)

**Estado:** Eliminada
**Resumen:** Primera aproximación basada únicamente en reglas estáticas.
**Motivo de deprecación:** La arquitectura no permitía escalabilidad ni integración con modelos de decisión más complejos.

---

## Versión 2

**Estado:** Vigente (Estructura heredada)
**Cambios clave:**

* Integración de un modelo básico de *Machine Learning* para mejorar la toma de decisiones.
* Soporte para múltiples divisas.
* Refactorización parcial del motor de reglas.

**Motivo de existencia:** Fue el primer salto significativo más allá de simples reglas, y sentó las bases de la lógica actual.

---

## Versión 3 (Actual)

**Estado:** Versión recomendada
**Cambios clave:**

* Endurecimiento del módulo de seguridad.
* Migración a una base de datos estructurada bajo estándares ISO relevantes en la banca:

  * **ISO 8583** para transacciones financieras.
  * **ISO 4217** para codificación de divisas.
* Optimización de la arquitectura para facilitar auditoría, escalabilidad y cumplimiento normativo.

**Motivo de existencia:** Consolidar un sistema robusto alineado con prácticas del sector financiero.
