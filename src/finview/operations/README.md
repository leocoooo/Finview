# Module Operations

## Vue d'ensemble

Le module `operations` fournit une API propre et robuste pour effectuer des opérations sur un portfolio. Il remplace l'ancien système de monkey patching qui ajoutait dynamiquement des méthodes à la classe `Portfolio`.

## Structure

```
operations/
├── __init__.py              # Exports principaux
├── cash_operations.py       # Opérations sur le cash
├── investment_operations.py # Opérations sur les investissements
├── credit_operations.py     # Opérations sur les crédits
└── legacy.py               # Compatibilité avec l'ancien système (DEPRECATED)
```

## Utilisation

### Opérations sur le cash

```python
from src.finview.operations import add_cash, withdraw_cash
from datetime import datetime

# Ajouter du cash
add_cash(portfolio, 1000.0, datetime.now(), "Monthly salary")

# Retirer du cash
withdraw_cash(portfolio, 500.0, datetime.now(), "ATM withdrawal")
```

### Opérations sur les investissements financiers

```python
from src.finview.operations import add_financial_investment, update_investment_value, sell_investment

# Acheter un investissement
add_financial_investment(
    portfolio, 
    name="Apple Stock",
    initial_value=150.0,
    quantity=10,
    date=datetime.now(),
    investment_type="Stock",
    location="United States"
)

# Mettre à jour la valeur
update_investment_value(portfolio, "Apple Stock", 160.0, datetime.now())

# Vendre partiellement
sell_investment(portfolio, "Apple Stock", 5, datetime.now())
```

### Opérations sur l'immobilier

```python
from src.finview.operations import add_real_estate_investment

add_real_estate_investment(
    portfolio,
    name="Paris Apartment SCPI",
    initial_value=200.0,
    quantity=25,
    date=datetime.now(),
    property_type="SCPI",
    location="Paris",
    rental_yield=4.5
)
```

### Opérations sur les crédits

```python
from src.finview.operations import add_credit, pay_credit

# Contracter un crédit
add_credit(
    portfolio,
    name="Car Loan",
    amount=15000.0,
    interest_rate=2.8,
    monthly_payment=320.0,
    date=datetime.now()
)

# Effectuer un paiement
pay_credit(portfolio, "Car Loan", 320.0, datetime.now())
```

## Avantages par rapport à l'ancien système

### Ancien système (DEPRECATED)
```python
# ❌ Monkey patching - Mauvaise pratique
Portfolio._add_investment_with_date = _add_investment_with_date
portfolio._add_investment_with_date("Apple", 150.0, 10, datetime.now())
```

### Nouveau système
```python
# ✅ API fonctionnelle propre
add_financial_investment(portfolio, "Apple", 150.0, 10, datetime.now())
```

**Bénéfices :**
1. **Clarté** : Les fonctions sont explicites et documentées
2. **Validation** : Toutes les entrées sont validées avec des messages d'erreur clairs
3. **Testabilité** : Fonctions pures faciles à tester
4. **Type safety** : Signatures de fonction claires avec type hints
5. **Pas de mutation de classe** : Respecte les principes SOLID

## Gestion d'erreurs

Toutes les fonctions peuvent lever des `ValueError` avec des messages explicites :

```python
try:
    add_financial_investment(portfolio, "", 150.0, 10)  # Nom vide
except ValueError as e:
    print(e)  # "Le nom de l'investissement ne peut pas être vide"

try:
    add_financial_investment(portfolio, "Apple", -150.0, 10)  # Prix négatif
except ValueError as e:
    print(e)  # "Le prix unitaire doit être positif, reçu: -150.0"

try:
    sell_investment(portfolio, "Inexistant", 5)  # N'existe pas
except ValueError as e:
    print(e)  # "Investissement 'Inexistant' introuvable"
```

## Migration depuis l'ancien système

### Avant (ancien système)
```python
portfolio._add_cash_with_date(1000.0, date, "Bonus")
portfolio._add_financial_investment_with_date("Tesla", 200.0, 5, date, "Stock", "US")
portfolio._update_investment_with_date("Tesla", 220.0, date)
portfolio._pay_credit_with_date("Loan", 500.0, date)
```

### Après (nouveau système)
```python
add_cash(portfolio, 1000.0, date, "Bonus")
add_financial_investment(portfolio, "Tesla", 200.0, 5, date, "Stock", "US")
update_investment_value(portfolio, "Tesla", 220.0, date)
pay_credit(portfolio, "Loan", 500.0, date)
```

**Note :** Le paramètre `date` est optionnel. Si omis, `datetime.now()` est utilisé.

## Compatibilité

Le module `operations.legacy` fournit des wrappers pour maintenir la compatibilité avec l'ancien code. Ces fonctions émettent des avertissements de dépréciation et devraient être remplacées progressivement.

```python
# Toujours supporté mais DEPRECATED
from src.finview.operations.legacy import _add_investment_with_date
# ⚠️ DeprecationWarning: _add_investment_with_date is deprecated, use operations.add_financial_investment() instead
```

## Historique des transactions

Toutes les opérations enregistrent automatiquement une entrée dans `portfolio.transaction_history` avec :
- `date` : Date/heure de l'opération
- `type` : Type d'opération (CASH_ADD, INVESTMENT_BUY, etc.)
- `amount` : Montant de la transaction
- `name` : Nom de l'asset (si applicable)
- `price` : Prix unitaire (si applicable)
- `quantity` : Quantité (si applicable)
- `description` : Description lisible de l'opération

## Types d'opérations

### Cash
- `CASH_ADD` : Ajout de cash
- `CASH_WITHDRAW` : Retrait de cash

### Investissements
- `FINANCIAL_INVESTMENT_BUY` : Achat d'investissement financier
- `REAL_ESTATE_INVESTMENT_BUY` : Achat d'investissement immobilier
- `INVESTMENT_UPDATE` : Mise à jour de valeur
- `INVESTMENT_SELL` : Vente d'investissement

### Crédits
- `CREDIT_ADD` : Nouveau crédit
- `CREDIT_PAYMENT` : Paiement sur un crédit

## Bonnes pratiques

1. **Toujours valider les entrées utilisateur** avant d'appeler les opérations
2. **Utiliser try/except** pour gérer les erreurs de manière appropriée
3. **Fournir des descriptions claires** pour l'historique des transactions
4. **Éviter d'appeler les fonctions legacy** - migrer vers la nouvelle API
5. **Tester les opérations** avec des données de test avant de les utiliser en production

