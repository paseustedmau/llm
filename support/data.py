"""Base de conocimiento y datos ficticios usados por la demostración."""

from __future__ import annotations

from typing import Any


ORDERS: dict[str, dict[str, Any]] = {
    "LUM-1042": {
        "status": "En tránsito",
        "product": "Lámpara Nube",
        "estimated_delivery": "18 de julio",
        "carrier": "Estafeta",
        "tracking": "EST-884120",
    },
    "LUM-2088": {
        "status": "Entregado",
        "product": "Set Café Amanecer",
        "estimated_delivery": "Entregado el 12 de julio",
        "carrier": "DHL",
        "tracking": "DHL-552091",
    },
    "LUM-3301": {
        "status": "Preparando envío",
        "product": "Manta Sierra",
        "estimated_delivery": "21 de julio",
        "carrier": "Pendiente de asignar",
        "tracking": "Pendiente",
    },
}

POLICIES = {
    "envios": (
        "Los pedidos se preparan en 1–2 días hábiles. El envío estándar tarda "
        "3–5 días hábiles en México y es gratuito a partir de $999 MXN."
    ),
    "devoluciones": (
        "Se aceptan devoluciones durante 30 días naturales después de la entrega. "
        "El artículo debe conservar etiquetas y estar sin uso."
    ),
    "garantia": (
        "Los productos tienen garantía de 90 días por defectos de fabricación. "
        "Daños por uso indebido no están cubiertos."
    ),
    "pagos": (
        "Aceptamos tarjetas Visa, Mastercard y American Express, además de PayPal. "
        "Nunca solicitamos números completos de tarjeta por el chat."
    ),
}


def lookup_order(order_id: str) -> dict[str, Any]:
    """Consulta un pedido ficticio sin exponer información personal."""
    normalized = order_id.strip().upper()
    order = ORDERS.get(normalized)
    if not order:
        return {
            "found": False,
            "order_id": normalized,
            "message": "No encontramos ese pedido en la base de datos de demostración.",
        }
    return {"found": True, "order_id": normalized, **order}


def search_policy(topic: str) -> dict[str, str | bool]:
    """Busca una política por tema y devuelve una respuesta verificable."""
    normalized = topic.strip().lower()
    aliases = {
        "envío": "envios",
        "envios": "envios",
        "envíos": "envios",
        "devolución": "devoluciones",
        "devoluciones": "devoluciones",
        "garantía": "garantia",
        "garantia": "garantia",
        "pago": "pagos",
        "pagos": "pagos",
    }
    key = aliases.get(normalized)
    if not key:
        return {"found": False, "topic": normalized, "message": "Tema no disponible."}
    return {"found": True, "topic": key, "policy": POLICIES[key]}


def create_support_ticket(reason: str, priority: str = "normal") -> dict[str, str]:
    """Simula el escalamiento a una persona del equipo de soporte."""
    safe_priority = priority if priority in {"normal", "alta"} else "normal"
    return {
        "created": "true",
        "ticket_id": "CASO-7421",
        "priority": safe_priority,
        "reason": reason[:180],
        "next_step": "Una persona del equipo responderá por correo en menos de 24 horas.",
    }

