最后一步还未完成，
 File "D:\workspace\prePostgraduate\DJango-Learning\FairnessAuditing\models\metrics.py", line 38, in individual_unfairness
    all_pred = model.get_prediction(samples)
               ^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AuditingFramework' object has no attribute 'get_prediction'
metrics.py显示main函数缺少get_prediction方法
