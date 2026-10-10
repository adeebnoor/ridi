# Coding manual — RIDI-PREDICT-v1 (frozen with the preregistration)
# دليل الترميز للمساعدَين البحثيَّين

## General rules / قواعد عامة

- **EN:** Code alone. Do not discuss items with the other coder until both sheets are submitted. Do not search the web. Use only the text shown. If unsure, choose the more conservative option and write a note.
- **AR:** كل واحد يرمّز لحاله. لا تتناقشون في أي عنصر قبل ما يسلّم الاثنان أوراقهم. لا تبحثون في الإنترنت، واعتمدوا فقط على النص المعروض. إذا ترددت، اختر الخيار الأكثر تحفظاً واكتب ملاحظة.

- **EN:** Do not use ChatGPT, Claude or any other AI tool, translator or search engine. The point of this task is an independent human judgement.
- **AR:** لا تستخدموا ChatGPT أو Claude أو أي أداة ذكاء اصطناعي أو مترجم آلي أو محرك بحث. الهدف من المهمة حكم بشري مستقل.
- **EN:** Do not share the sheets or the passages with anyone. Start only when the PI confirms in writing that the ethics determination allows it.
- **AR:** لا تشاركوا الأوراق أو المقاطع مع أحد. ولا تبدؤون إلا بعد تأكيد مكتوب من الباحث الرئيسي أن قرار لجنة الأخلاقيات يسمح بذلك.

**EN — what the sheets do not show:**
- which items are of interest;
- model answers;
- any automated labels.

Do not try to guess them.

**AR — ما لا تعرضه الأوراق:**
- العناصر المهمة؛
- إجابات النماذج؛
- أي تصنيفات آلية.

لا تحاولوا تخمينها.

**EN:** Expected time is about 1 minute per item in Part A and about 2–3 minutes per item in Part B.
**AR:** الوقت المتوقع: حوالي دقيقة للعنصر في الجزء A، ومن دقيقتين إلى ثلاث في الجزء B.

---

## Part A — one passage per row / مقطع واحد في كل سطر

Each row shows a question, its accepted gold answer(s) and one passage. For claim rows (a statement instead of a question) the "gold answer" is the verdict on the claim: SUPPORTS, REFUTES or NOT_ENOUGH_INFO.
كل سطر فيه سؤال، وإجابته المقبولة، ومقطع واحد. في أسطر الادعاءات (جملة بدل سؤال) تكون «الإجابة» هي الحكم على الادعاء: يؤيد، ينفي، أو معلومات غير كافية.

**A. Does the passage answer or decide the question? / هل المقطع يجيب على السؤال أو يحسمه؟**

- **yes / نعم:** A careful reader could give the gold answer, or decide a claim as SUPPORTED or REFUTED, from this passage alone.
  قارئ متأنٍ يقدر يعطي الإجابة الصحيحة، أو يحكم على الادعاء بالتأييد أو النفي، من هذا المقطع وحده.
- **partly / جزئياً:** The passage gives a necessary piece but not the whole answer. Examples: one hop of a two-hop question; a related fact that narrows the answer.
  المقطع يعطي جزءاً ضرورياً من الإجابة لا كلها. مثال: خطوة واحدة من سؤال يحتاج خطوتين، أو معلومة قريبة تضيّق الاحتمالات.
- **no / لا:** Nothing in the passage helps answer the question.
  لا شيء في المقطع يساعد في الإجابة.

**B. Does the passage contain the gold-answer string? / هل يحتوي المقطع نص الإجابة؟**

- **EN:** yes or no. Ignore case and punctuation. For claim rows (gold answer SUPPORTS / REFUTES / NOT_ENOUGH_INFO), always answer "no".
- **AR:** نعم أو لا. تجاهل حالة الأحرف وعلامات الترقيم. وفي أسطر الادعاءات تكون الإجابة دائماً «لا».

**C. Is the passage on the same topic as the question? / هل المقطع في نفس موضوع السؤال؟**

- **EN:** yes or no.
- **AR:** نعم أو لا.

---

## Part B — one question per row / سؤال واحد في كل سطر

Each row shows a question, its gold answer(s) and the ten passages the system retrieved.
كل سطر فيه سؤال، وإجابته المقبولة، والمقاطع العشرة التي استرجعها النظام.

Answer every item yes or no. / أجب عن كل بند بنعم أو لا.

1. **More than one defensible answer.** A reasonable expert could give a different answer and still be right, for example because of date, granularity or naming.
   **أكثر من إجابة مقبولة:** خبير معقول قد يعطي إجابة مختلفة وتكون صحيحة أيضاً، بسبب التاريخ أو درجة التفصيل أو صيغة التسمية مثلاً.
2. **Needs two or more passages.** No single passage is sufficient, but a combination is.
   **يحتاج مقطعين أو أكثر:** لا يكفي مقطع واحد، لكن الجمع بينها يكفي.
3. **Conflicting passages.** At least two passages point to different answers.
   **تعارض بين المقاطع:** مقطعان على الأقل يشيران إلى إجابتين مختلفتين.
4. **Underspecified question.** The question lacks information needed to pin down one answer.
   **سؤال ناقص التحديد:** السؤال ينقصه ما يلزم لتحديد إجابة واحدة.
5. **Debatable gold answer.** The gold answer looks wrong, incomplete or outdated given the passages.
   **إجابة مرجعية قابلة للنقاش:** الإجابة المرجعية تبدو خاطئة أو ناقصة أو قديمة، بالنظر إلى المقاطع.

---

## After coding / بعد الانتهاء

- **EN:** Both coders submit their sheets to the PI. The PI computes agreement (Cohen's κ) and then holds one meeting where the coders resolve disagreements. Both the original codes and the resolved codes are kept.
- **AR:** يسلّم الاثنان أوراقهما للباحث الرئيسي. يحسب الباحث نسبة الاتفاق (كوهين كابا)، ثم يعقد جلسة واحدة يحل فيها المرمّزان الخلافات. وتُحفظ الرموز الأصلية والرموز بعد الحل كلاهما.
