"""
accounts/templatetags/school_tags.py

Filtres de template personnalisés pour G-Scolaire.
Usage dans les templates :
    {% load school_tags %}
    {{ montant|fcfa }}          → "150 000 FCFA"
    {{ montant|fcfa_court }}    → "150 000 F"
    {{ montant|fcfa_signe }}    → "+ 150 000 FCFA" / "- 150 000 FCFA"
"""

from django import template

register = template.Library()


def _format_number(value):
    """Formate un nombre avec séparateur de milliers (espace)."""
    try:
        n = int(round(float(value)))
    except (TypeError, ValueError):
        return "0"
    # Séparateur de milliers par espace
    s = f"{n:,}".replace(",", "\u202f")  # espace insécable
    return s


@register.filter(name="fcfa")
def fcfa(value):
    """Affiche un montant en FCFA : ex. 150 000 FCFA"""
    return f"{_format_number(value)} FCFA"


@register.filter(name="fcfa_court")
def fcfa_court(value):
    """Version courte : ex. 150 000 F"""
    return f"{_format_number(value)} F"


@register.filter(name="fcfa_signe")
def fcfa_signe(value):
    """Avec signe +/- : ex. +150 000 FCFA"""
    try:
        n = float(value)
    except (TypeError, ValueError):
        return "0 FCFA"
    signe = "+" if n >= 0 else ""
    return f"{signe}{_format_number(abs(n))} FCFA"


@register.filter(name="nombre")
def nombre(value):
    """Formate un nombre avec séparateur de milliers uniquement."""
    return _format_number(value)
