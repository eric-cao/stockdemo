from django.db import models

class Stock(models.Model):
    idstock_detail = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=45)
    date = models.DateField()
    open = models.DecimalField(..., max_digits=15, decimal_places=6)
    close = models.DecimalField(..., max_digits=15, decimal_places=6)
    low = models.DecimalField(..., max_digits=15, decimal_places=6)
    high = models.DecimalField(..., max_digits=15, decimal_places=6)
    adj_close = models.DecimalField(..., max_digits=15, decimal_places=6)
    volume = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock_detail'
