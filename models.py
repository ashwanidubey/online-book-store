from django.db import models
from django.contrib.auth.models import User,auth
class Book(models.Model):
    user=models.ManyToManyField(User,through="Transaction")
    book_id=models.AutoField(primary_key=True)
    book_name=models.CharField(max_length=100)
    pub_date=models.DateField(auto_now_add=True)
    book_price=models.FloatField()
    book_author=models.CharField(max_length=100)
    book_publication=models.CharField(max_length=100)
    book_status=models.CharField(max_length=12 , default="AVAILABLE")
    book_copy=models.PositiveIntegerField(default=0b001)
    def __str__(self):
        return self.book_name
class Transaction(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    T_id=models.AutoField(primary_key=True)
    T_idd=models.CharField(default='00',max_length=14)
    #id=models.CharField(max_length=25 ,default="TRAN"+'0'*(10-len(str(T_id)))+str(T_id))
    T_date=models.DateField(auto_now_add=True )
    T_time=models.TimeField(auto_now_add=True )
    R_status=models.CharField(max_length=25 ,default="not returned")
    R_date=models.DateField(null=True)
    def __str__(self):
        return 'TRAN'+'0'*(10-len(str(self.T_id)))+str(self.T_id)
