from rest_framework import serializers
from collections import defaultdict
from apps.dashboard.models import CexQuotes
from datetime import datetime

class CexReportSerializer(serializers.Serializer):
    data = serializers.ListField()

    @staticmethod
    def organize_quotes_by_date(queryset):
        """
        Organiza las cotizaciones por año y mes, generando count mensual y totalCount acumulado en general.
        Solo devuelve los últimos 12 meses, pero el totalCount debe incluir meses anteriores.
        """
        data = defaultdict(int)  # 🔹 Diccionario que almacena el conteo de cotizaciones por mes
        grand_total_count = 0  # 🔹 Contador global acumulado desde el primer mes
        all_months = []  # 🔹 Lista para almacenar todas las fechas disponibles

        for quote in queryset:
            quote_date = quote.quoted_on  # Fecha de la cotización
            
            # 🔹 Convertir la fecha si es string
            if isinstance(quote_date, str):
                try:
                    quote_date = datetime.strptime(quote_date, "%Y-%m-%d %H:%M:%S.%f")  # Con milisegundos
                except ValueError:
                    quote_date = datetime.strptime(quote_date, "%Y-%m-%d %H:%M:%S")  # Sin milisegundos
            
            # 🔹 Extraer año y mes en formato `YYYY-MM` para mantener un orden correcto
            year_month = quote_date.strftime("%Y-%m")

            data[year_month] += 1  # 🔹 Incrementar la cuenta de cotizaciones para ese mes
            all_months.append(year_month)  # Guardar todas las fechas únicas registradas

        # 🔹 Obtener todos los meses ordenados cronológicamente
        sorted_months = sorted(set(all_months))

        # 🔹 Calcular `grand_total_count` desde el inicio
        total_count_by_month = {}  # 🔹 Diccionario para almacenar el total acumulado por cada mes
        for i, year_month in enumerate(sorted_months):
            grand_total_count += data[year_month]  # Acumular todas las cotizaciones desde el primer mes
            total_count_by_month[year_month] = grand_total_count  # Guardar el total acumulado hasta ese mes

        # 🔹 Obtener los últimos 12 meses
        last_12_months = sorted_months[-12:]

        # 🔹 Convertir a formato JSON con `totalCount` acumulado desde el inicio
        result = []
        for year_month in last_12_months:
            year, month_number = map(int, year_month.split("-"))  # Extraer año y mes en números
            month_name = datetime(year, month_number, 1).strftime("%B")  # Convertir número a nombre de mes
            count = data[year_month]  # Obtener el total de ese mes
            
            # 🔹 Agregar al resultado
            result.append({
                "year": year,
                "month": month_name,
                "count": count,
                "totalCount": total_count_by_month[year_month]  # 🔹 Ahora incluye los meses no mostrados
            })
        
        return {"data": result}  # 🔹 Envolver en un diccionario para evitar errores

    def to_representation(self, instance):
        return self.organize_quotes_by_date(instance)
