from transformers import BertForSequenceClassification, TrainingArguments, Trainer
import evaluate
import numpy as np

model = BertForSequenceClassification.from_pretrained('ahmedrachid/FinancialBERT', num_labels=3)  # Angenommene 3 Labels: bullish, neutral, bearish

accuracy = evaluate.load("accuracy")
f1_score = evaluate.load("f1")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    acc = accuracy.compute(predictions=predictions, references=labels)
    f1 = f1_score.compute(predictions=predictions, references=labels)
    return {
        'accuracy': acc,
        'f1': f1
    }

trainings_args = TrainingArguments(
    output_dir='./results',
    learning_rate=2e-5,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=300,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10
)

trainer = Trainer(
    model = model,
    args = trainings_args,
    train_dataset = train_dataset,
    eval_dataset = val_dataset,
    tokenizer = tokenizer,
    compute_metrics = compute_metrics
)

trainer.train()