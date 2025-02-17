from decimal import Decimal

class MonedaUtils:
    
    _iva= Decimal(0.16)


    @staticmethod
    def aplicar_descuentos_en_cascada(importe, *descuentos):
        """
        Aplica los descuentos en cascada a un importe.

        Args:
            importe (Decimal): El importe al que se le aplicarán los descuentos.
            *descuentos (Decimal): Los descuentos a aplicar en cascada.

        Returns:
            Decimal: El importe con los descuentos aplicados.
        """
        for descuento in descuentos:
            importe = round(importe*(1-(descuento/100)),2)
        return importe
    
    @staticmethod
    def calcular_iva(importe):
        """
        Calcula el IVA de un importe.

        Args:
            importe (Decimal): El importe al que se le calculará el IVA.

        Returns:
            Decimal: El IVA del importe.
        """
        return round(importe * MonedaUtils._iva,2)