# James Stanier — Distilled Principles

Source material: 161 blog posts at theengineeringmanager.substack.com (2017-06-28 → 2026-05-15). Author: James Stanier — engineering manager → director → VP → CTO. Books: *Become an Effective Software Engineering Manager*, *Effective Remote Work*.

Coverage notes:
- 2017: 25 posts (founding-EM era, Grove-heavy)
- 2018: 45 posts (deepening EM craft, remote turn)
- 2019-2021: 36 posts (senior EM → director, full remote era, COVID)
- 2022-2024: 32 posts (director/VP, mature frameworks, leading-edge org thinking)
- 2025-2026: 23 posts (CTO, AI-era operator stance) — weighted 2x

## Decision-making, focus & action speed

### Dead time is the enemy

While a decision sits open it accrues opinions, complications and cost. Hold yourself accountable for the speed of decision-making, not just its quality.

**Recurring evidence:** 2018-02-16_failing-fast.md, 2023-04-15_fast-forwarding-decision-making.md, 2017-11-19_cadence.md, 2018-03-03_letting-go.md

> "The longer that a decision goes unmade, the more value that it gains, for better or for worse. Unmade decisions attract ever *more* opinions and become more diluted and complicated and harder to execute." — 2018-02-16_failing-fast.md

> "hold yourself accountable for making decisions and progressing discussions as quickly as possible, by whatever means necessary. Be *restless* while a decision hasn't been made. Dead time is your enemy." — 2023-04-15_fast-forwarding-decision-making.md

### Lead with the recommendation

In the opening seconds of any written or verbal interaction the other person should know what you want. Don't make them reconstruct your viewpoint from raw evidence — give them one to interrogate.

**Recurring evidence:** 2022-10-29_get-straight-to-the-point.md, 2018-08-02_that-massive-email.md, 2025-08-30_going-direct.md

> "Ideally, within the opening seconds of an interaction—written or verbal—the other person should know exactly what you want." — 2022-10-29_get-straight-to-the-point.md

> "**But if you already have a recommendation, say it up front.**" — 2022-10-29_get-straight-to-the-point.md

> "Encourage them to follow a simple structure: *context, problem, and a clear ask*." — 2025-08-30_going-direct.md

### Focus is saying no to the hundred other good ideas

A single ordered list, no ties allowed, is the forcing function. People naturally solve B+ problems they know how to solve instead of A+ problems that are difficult — single-threaded leadership exists to prevent that drift.

**Recurring evidence:** 2026-02-13_one-list-to-rule-them-all.md, 2017-11-19_cadence.md, 2018-08-16_algorithms-to-make-you-more-effective.md, 2020-09-12_bucketing-your-time.md

> "'People think focus means saying yes to the thing you've got to focus on,' he said. 'But that's not what it means at all. It means saying no to the hundred other good ideas that there are.'" — 2026-02-13_one-list-to-rule-them-all.md

> "Thiel understood that most people will solve problems that they understand how to solve, which means, in his words, that they will solve B+ problems instead of A+ problems. A+ problems are high impact, but they're difficult, and you cannot immediately derive a solution, so you tend to procrastinate." — 2026-02-13_one-list-to-rule-them-all.md

> "As a leader you will need to practice saying no to incoming demands so that you can keep your projects moving at an acceptable pace." — 2017-11-19_cadence.md

### Fix one bottleneck at a time

Every system has exactly one constraint. Improving anything else doesn't improve the system. Subordinate everything else to the bottleneck — including putting your best people on the ugliest work.

**Recurring evidence:** 2026-01-14_one-bottleneck-at-a-time.md, 2025-09-30_the-beauty-of-constraints.md

> "The core insight is simple: every system, whether it's a factory or a software team, has exactly one constraint that limits its overall throughput at any given time. Improving anything other than that constraint doesn't improve the system." — 2026-01-14_one-bottleneck-at-a-time.md

> "This feels counterintuitive, and you'll face resistance, because we naturally want to point our highest performers at the sexiest problems, not the ugliest ones. But constraints are often the ugliest problems, and changing this cultural instinct is part of the work of leadership, because high performers turn *ugly* work into *beautiful* work." — 2026-01-14_one-bottleneck-at-a-time.md

### Fail fast — push uncertainty upstream

Every project is an iceberg with 90% underwater. Align the team around continually reducing uncertainty, not just shipping. Tackle the most uncertain parts first — leaving them till last guarantees scope blowup at the deadline.

**Recurring evidence:** 2018-02-16_failing-fast.md, 2022-11-26_removing-uncertainty-the-tip-of-the.md, 2018-08-30_dont-make-your-staff-afraid-to-fail.md, 2025-09-30_the-beauty-of-constraints.md

> "The more value that has been added to a component, the less reusable it is, and the more there is to lose when failure occurs. It is more expensive to fail further down the production line." — 2018-02-16_failing-fast.md

> "When you're staring a huge, challenging project in the face, don't align your team around just getting it done. Instead, align your team around **continually reducing uncertainty**." — 2022-11-26_removing-uncertainty-the-tip-of-the.md

> "The worst project crunch happens when uncertainty *hasn't* been stripped away up front. If you leave the most uncertain parts until last, you'll be dealing with them right before the deadline, and the most uncertain parts always have the biggest probability of blowing up in scope and complexity." — 2022-11-26_removing-uncertainty-the-tip-of-the.md

### Forecast, don't commit — dates are one-way doors

Trust drops faster than people realise when an over-specific date slips. Start wide (year), taper to quarter then month as uncertainty drops, only land on a specific date when uncertainty is near zero.

**Recurring evidence:** 2024-09-29_what-does-a-date-actually-mean.md, 2017-11-02_the-stick.md, 2025-08-30_going-direct.md

> "From a psychological perspective, this is because the lowest level of granularity is often a *one-way door*." — 2024-09-29_what-does-a-date-actually-mean.md

> "you should take a forecasting approach that follows the uncertainty curve that we outlined above. You start wide, and you taper in. At the beginning of a given project, you might even just have the year that you're aiming to ship." — 2024-09-29_what-does-a-date-actually-mean.md

> "Setting fake deadlines is a terrible idea: they'll see through your deception. Telling them to work harder and faster with no clear reason or purpose will make you look stupid." — 2017-11-02_the-stick.md

### Invert, always invert — apply deliberate pessimism

Default planning is too optimistic. Before launching anything significant, run an inversion pass: ask what would have to happen for this to fail, then triage findings into showstopper / mitigation / accepted.

**Recurring evidence:** 2025-11-23_invert-always-invert.md, 2018-04-22_first-principles-and-asking-why.md, 2025-07-31_leadership-co-processing-with-llms.md

> "Munger adapts this into practical situations: to succeed at an outcome, you should invert it by thinking about what would have to happen for you to *fail*, and then completely avoid all of those things in order to succeed." — 2025-11-23_invert-always-invert.md

> "Make it clear that no idea is too pessimistic, and that today we are being paid to be cynics." — 2025-11-23_invert-always-invert.md

> "I like to employ an LLM as a contrarian thinker whenever I need to make a controversial decision or ensure that what I am thinking is not just a confirmation of my own biases." — 2025-07-31_leadership-co-processing-with-llms.md

### Slow down to speed up — deliberation matters more when execution is cheap

When AI accelerates building, the leverage moves to the decisions before it. Bad inputs propagate faster. Timebox the slow phase, use AI to accelerate deliberation, build throwaway prototypes to validate direction before investing weeks.

**Recurring evidence:** 2026-03-13_slow-down-to-speed-up.md, 2025-09-30_the-beauty-of-constraints.md, 2017-12-05_mount-stupid.md

> "And here's the counterintuitive and highly interesting part: AI didn't make the slow phases less important, it made them *more* important. When execution is cheap and fast, the leverage shifts to the decisions that precede it." — 2026-03-13_slow-down-to-speed-up.md

> "A wrong requirement, a misunderstood problem, a flawed design assumption: these propagate through everything AI helps you build, only now they propagate *faster*. The cost of getting System 2 wrong goes up precisely because System 1 has become so powerful." — 2026-03-13_slow-down-to-speed-up.md

> "Question the requirements. Musk says that the most common error of a smart engineer is to *optimize things that shouldn't exist in the first place*. He stipulates that smart folk are trained to answer questions, but not to challenge the questions in the first place." — 2025-09-30_the-beauty-of-constraints.md

## People, coaching & feedback

### 1:1s are not status updates — they're for coaching

With time and without conscious effort, all 1:1s degenerate into status updates. They have no place in your life if that's all they are. Move status to async channels; spend the synchronous slot on development, career and the biggest problems.

**Recurring evidence:** 2017-06-28_121s.md, 2018-05-18_keeping-your-1-to-1s-fresh.md, 2020-10-11_less-status-updates-more-coaching.md

> "*With time, and without conscious effort, all 1 to 1 meetings will degenerate into status updates.* Can we call that Stanier's Law?" — 2018-05-18_keeping-your-1-to-1s-fresh.md

> "1 to 1s that are nothing but status updates have no place in your life. They're boring, they don't contribute to either of your personal development, and they're just a repeat of information that could be better recorded and broadcast elsewhere." — 2018-05-18_keeping-your-1-to-1s-fresh.md

> "When you're managing managers, the best use of your time is **coaching**: that is, guiding your staff to work out the solutions to their own problems." — 2020-10-11_less-status-updates-more-coaching.md

### Care personally + challenge directly (Radical Candor)

The combination is what makes feedback land. Caring without challenging is ruinous empathy; challenging without caring is obnoxious aggression. Both halves are required.

**Recurring evidence:** 2017-08-11_giving-feedback.md, 2022-07-24_how-do-i-get-better-at-giving-feedback.md, 2018-01-30_leadership-through-kindness.md

> "Kim Scott's excellent book Radical Candor distills the traits of giving good feedback into two simple categories: '*Care Personally*' and '*Challenge Directly*'. When these two traits are combined in the relationship between a manager and their direct reports, the right atmosphere is in place to criticize, praise and push people to perform at a high level." — 2017-08-11_giving-feedback.md

> "**Radical candor is what happens when you care personally and challenge someone directly.** You say what you think and deliver the feedback precisely but in such a way that ensures the recipient sees that you are doing so because you care." — 2022-07-24_how-do-i-get-better-at-giving-feedback.md

> "Being kind doesn't mean letting standards slip, or accepting poor performance, or protecting your staff from interacting with difficult personalities or projects." — 2018-01-30_leadership-through-kindness.md

### Nine out of ten feedback should be positive

If you're hunting for opportunities, most of what you give is positive. Star performers wither without it — don't let your attention drift to the strugglers and starve the top.

**Recurring evidence:** 2017-08-11_giving-feedback.md, 2022-07-24_how-do-i-get-better-at-giving-feedback.md

> "Your best performers will want consistent feedback that they are doing well and that you appreciate the effort that they are putting in." — 2017-08-11_giving-feedback.md

> "As a rule of thumb, I find that nine out of ten pieces of feedback I give are always positive if I'm actively looking out for the opportunities to give them." — 2022-07-24_how-do-i-get-better-at-giving-feedback.md

### Push the thought bubble back over their head

When coaching, fight the urge to solve. Imagine the cartoon thought bubble over your head and push it physically over theirs. Ask another question. Let them arrive at the answer.

**Recurring evidence:** 2017-12-21_coaching.md, 2017-06-28_121s.md, 2020-10-11_less-status-updates-more-coaching.md

> "Even if you are the world's most expert engineer, don't tell them what to do, especially if you know what the solution is. Instead, every time that you feel that you would naturally jump in and solve a problem, imagine yourself pushing a big cartoon thought bubble away from your own head and putting it over theirs." — 2017-12-21_coaching.md

> "Try and get your direct report to do 70% of the talking. If you feel like solving their problem for them, don't. Ask another question and let them arrive at the conclusion themselves." — 2017-06-28_121s.md

> "**Continually pushing the thought bubble back over their head** by asking open-ended questions so that they are able to find the answers to their own problems (see: [rubber ducking](https://en.wikipedia.org/wiki/Rubber_duck_debugging))." — 2020-10-11_less-status-updates-more-coaching.md

### Delegate the how, control the what — never abdicate

Delegation transfers responsibility while you retain accountability. When you don't know what's going on, you've abdicated, not delegated.

**Recurring evidence:** 2017-08-04_delegation.md, 2018-03-03_letting-go.md, 2023-11-07_its-all-just-leadership-after-all.md, 2024-11-30_being-in-the-details.md

> "Firstly, delegating is not a 'fire and forget' activity. As Grove points out, it is not abdication. It's not like receiving an email and then immediately forwarding it to someone else." — 2017-08-04_delegation.md

> "What you keep within your close control is ownership of the *target* that your direct reports are aiming for, but you let them choose exactly *how* they choose to hit it." — 2023-11-07_its-all-just-leadership-after-all.md

> "when you don't know what's going on, you've not actually delegated: you've *abdicated*." — 2024-11-30_being-in-the-details.md

### Leadership is disappointing people at a rate they can absorb

There is always a void between desire and reality. Don't shield the team from it — bubbles delay the inevitable, then make it worse. Be transparent about what you own; collaborate on what you don't.

**Recurring evidence:** 2024-05-24_the-disappointment-frontier.md, 2024-09-29_what-does-a-date-actually-mean.md, 2017-11-02_the-stick.md

> "Leadership *is* about disappointing people at a rate they can absorb. There's always a void between desire and reality." — 2024-05-24_the-disappointment-frontier.md

> "Keeping people and teams in a bubble of protection never ends well. It just delays the inevitable disappointment that will come when reality hits." — 2024-05-24_the-disappointment-frontier.md

> "Dates *mean* something to people, so handle them with care." — 2024-09-29_what-does-a-date-actually-mean.md

### People will leave — eliminate zingers

Surprise resignations trace back to communication failure. You're doomed if you try to keep everyone forever; the job is to read signals early and either fix the relationship or part well.

**Recurring evidence:** 2017-10-10_when-people-leave.md, 2018-05-10_job-hopping-and-what-you-can-do-about-it.md, 2017-06-28_121s.md

> "*People are always going to leave. It's normal and it sucks.* Just read it a few times and let it sink in. As a manager, you are doomed to failure if you think that you are going to keep everyone in your current team indefinitely." — 2017-10-10_when-people-leave.md

> "The bad situations I refer to are the ones [Andy Grove] called 'zingers'. What he was describing was the situation where you are caught completely off-guard by someone handing in their notice, insofar that you know in retrospect you could have prevented it from happening." — 2017-10-10_when-people-leave.md

> "If you think that you're able to *prevent* people from leaving then you're only going to feel extra bad when they eventually do. However, there are strategies that you can employ to *increase the likelihood* that people are going to stay for longer." — 2018-05-10_job-hopping-and-what-you-can-do-about-it.md

### Careers are squiggles, not ladders — coach beyond the next rung

Career tracks are local maxima of one company; they don't enumerate the possibilities of an entire career. Help reports work backwards from their global maxima, not toward the next dangling carrot.

**Recurring evidence:** 2022-07-17_how-do-i-progress-to-the-next-level.md, 2024-04-23_the-tarzan-method.md, 2024-06-25_deltas-to-the-global-maxima.md, 2017-11-27_your-career-is-your-responsibility.md, 2023-08-01_should-i-change-job.md

> "What careers really look like is a bit like a squiggle, rather than a ladder." — 2022-07-17_how-do-i-progress-to-the-next-level.md

> "Instead, you should think about your career like Tarzan swinging through the jungle. Tarzan starts at one tree and knows that he has an ultimate destination, but the path to get there isn't immediately clear" — 2024-04-23_the-tarzan-method.md

> "Given that career tracks represent a local maxima of a single company and not the enumeration of the possibilities of an entire career, the problem hampering many manager-report relationships is that *all coaching and personal development focus is limited to the next step on the ladder at the current company*, and nothing beyond that." — 2024-06-25_deltas-to-the-global-maxima.md

> "*\"At every job, you should either learn or earn. Either is fine. Both are best. But if it's neither, quit.\"*" — 2023-08-01_should-i-change-job.md

### Contracting — make explicit what each side needs

On every new relationship (new manager, new report), don't drift into it. Run an explicit exercise where both parties state what they need to operate well together. Pair with a manager handoff (1:1:1) when reports change manager.

**Recurring evidence:** 2017-07-20_managing-upwards.md, 2022-08-08_how-do-i-deal-with-my-manager-changing.md

> "By which means, and how often, would they like to be informed of: Weekly and daily progress on projects that you are accountable for; Something critically urgent happening (e.g. the entire app is down or someone wants to leave); Your staff's performance, good or bad; Administrative events such as your own sickness or needing to work from home" — 2017-07-20_managing-upwards.md

> "**I always recommend an exercise called contracting** ... The idea is that you're starting a brand new relationship and your first meeting together is an opportunity for both you and your new manager to make it really clear as to what you both need from each other in the relationship." — 2022-08-08_how-do-i-deal-with-my-manager-changing.md

### Catch performance issues early — direct and compassionate

Indirect probing lets bad performance fester until the review becomes a shock. The cycle: direct → compassionate → direct → open. Star performers can carry the team; tolerated under-performers signal a low bar to everyone else.

**Recurring evidence:** 2017-08-11_giving-feedback.md, 2017-06-28_121s.md, 2017-12-12_the-contribution-curve.md

> "Instead, Susan should have been direct as early as possible. This can be challenging but becomes easier with experience." — 2017-08-11_giving-feedback.md

> "This is especially true of performance issues which, when left alone for too long, become nearly impossible to repair." — 2017-06-28_121s.md

> "A net-negative poor performer has a bigger blast radius for their net-negativity compared to the previous examples because they are a drain on collective morale as well as the time and attention of other staff." — 2017-12-12_the-contribution-curve.md

## Self-management & personal operating system

### Externalise everything — the mind is unreliable

Calm comes from getting it out of your head and into systems you trust. The act of writing the weekly is journalism for the mind — it forces you to notice what needs attention.

**Recurring evidence:** 2017-07-07_feeling-productive.md, 2018-07-12_the-importance-of-writing.md, 2022-07-31_how-do-i-make-sure-my-work-is-visible.md, 2025-01-31_gather-decide-execute.md, 2026-04-23_my-cto-daily-driver.md

> "For me, the key to feeling productive is keeping as much information as possible, not in my head. This way I can rest easy that I have everything I need to remember written down somewhere, so I can operate in the present moment with as much calm as I can muster." — 2017-07-07_feeling-productive.md

> "**It has become a form of journalism for my mind**: each week I need to pay close attention to what is going on because I need to document it, and in turn, that helps me discover what needs more of my attention and then I can prioritise accordingly." — 2022-07-31_how-do-i-make-sure-my-work-is-visible.md

> "No matter how good the tools are that your company provides, having your *own* system that you trust and have complete ownership of is essential: it won't disappear one day because the company decided to switch to a different tool." — 2025-01-31_gather-decide-execute.md

### Manage capacity, not time

Quality of time matters more than quantity. Capacity is a function of energy levels — it depletes on draining work, replenishes on energising work. Permanently-busy leaders are mismanaging capacity, not winning at it.

**Recurring evidence:** 2023-10-15_manage-your-capacity-not-your-time.md, 2022-08-14_my-energy-is-a-linear-function-until.md, 2017-07-07_feeling-productive.md

> "it's not the *quantity* of time that you are able to juggle, assign and manage that matters, it's the *quality* of the time that you are able to spend on your tasks." — 2023-10-15_manage-your-capacity-not-your-time.md

> "your capacity is not a constant: it is a function of your energy levels." — 2023-10-15_manage-your-capacity-not-your-time.md

> "These folks are not managing their capacity effectively. They are not leaving enough unallocated breathing room for the impromptu events that happen every single day." — 2023-10-15_manage-your-capacity-not-your-time.md

### Your time is yours to defend

The mindset shift: your calendar is yours to control, not a default invitation. Block deep-work slots before others claim them. Carve out time to mentally walk the floor — iterate over every project and person you own and find what needs your attention.

**Recurring evidence:** 2019-02-28_carve-out-your-own-thinking-space.md, 2020-09-12_bucketing-your-time.md, 2023-10-15_manage-your-capacity-not-your-time.md

> "The mindset is that *your time is important, and you are completely within your rights to control your time to increase the value of what you work on.*" — 2019-02-28_carve-out-your-own-thinking-space.md

> "**Mentally 'walking the floor'.** In your head, iterate through all of the ongoing projects and areas of which you have ownership. What's going well? What could do with more immediate support from you?" — 2019-02-28_carve-out-your-own-thinking-space.md

> "you should aim for allocating a default workload that is not your full capacity, purposefully leaving some portion of your time unallocated. This is because you need to leave space for the unexpected, such as escalations, meetings, and other interruptions that will inevitably arise." — 2023-10-15_manage-your-capacity-not-your-time.md

### Delegate, automate, or forget it

Every recurring activity in your daily and weekly buckets must pass one of three tests. If none apply, it doesn't belong on your calendar.

**Recurring evidence:** 2020-09-12_bucketing-your-time.md, 2018-03-03_letting-go.md, 2020-10-04_delegation-creates-career-progression.md

> "**Delegate it** to someone else. **Automate it** so that it requires less of your active input. **Forget about it** if it really isn't an impactful activity." — 2020-09-12_bucketing-your-time.md

> "Unless it's something only you can do, you should be protecting your own time and delegating consistently to your staff." — 2018-03-03_letting-go.md

> "You solve that problem through **delegation of more of your own role to your direct reports**." — 2020-10-04_delegation-creates-career-progression.md

### Daily progress on one strategic item is the balance signal

If you've moved one impactful one-off forward every day for a month, your workload is balanced. If not, the busywork has won.

**Recurring evidence:** 2020-09-12_bucketing-your-time.md, 2026-02-13_one-list-to-rule-them-all.md, 2025-01-31_gather-decide-execute.md

> "Most importantly, looking back over the last month, I've almost always been able to make daily progress against one impactful strategic item, which is usually my indicator as to whether my workload is balanced correctly." — 2020-09-12_bucketing-your-time.md

> "A good rule of thumb to judge your progress in a system like this is by measuring what proportion of your gathering turns into decisions and actions that you then take. If you act on a lot of information that you're gathering, then you'll find that you are tuned into the right things and that you're adding value." — 2025-01-31_gather-decide-execute.md

### Read widely, apply selectively, share regardless

Your unique experience is the point — it matters precisely because it's yours. Don't be silenced by the oppressive weight of prior art. Raising the floor of the industry is a collective effort.

**Recurring evidence:** 2023-08-18_read-widely-apply-selectively-share.md, 2018-07-12_the-importance-of-writing.md, 2023-07-12_there-is-no-number-one-tip.md

> "So don't be discouraged. *Read widely, apply selectively, and share regardless.* There is always value in this approach." — 2023-08-18_read-widely-apply-selectively-share.md

> "Well, your opinion matters because of exactly that: it's *your* opinion. That's what makes it unique, and that is why it needs to be heard." — 2023-08-18_read-widely-apply-selectively-share.md

> "Be on the hunt for tools, not prescriptions." — 2023-07-12_there-is-no-number-one-tip.md

### Work doesn't have to be your everything

Role engulfment is the failure mode. Autonomy/Mastery/Purpose is a mindset, not a work thing — pursue it in life too. Long hours in knowledge work produce sloppy output, not more output.

**Recurring evidence:** 2018-09-20_work-doesnt-have-to-be-your-everything.md, 2019-03-14_are-we-more-than-our-jobs.md, 2019-04-18_the-rebellion-against-chinas-996-culture.md

> "If you derive your core purpose through your work and then your work ceases to exist, then *what are you?*" — 2018-09-20_work-doesnt-have-to-be-your-everything.md

> "There is a term for this: *role engulfment*. It is used to describe when one role - or identity - grows to become the dominant aspect from which one views themselves." — 2019-03-14_are-we-more-than-our-jobs.md

> "Working endlessly to a punishing schedule can make an individual less effective than if they were fewer less hours in a calmer manner. Tired employees can do sloppy work and introduce bugs that cause downtime and even more effort to fix." — 2019-04-18_the-rebellion-against-chinas-996-culture.md

## Organisation design, influence & cross-functional work

### Grove's equation is the unit of measure

A manager's output = the output of their organization + the output of the neighboring organizations under their influence. This is the e=mc² of management; everything you do should reduce to it.

**Recurring evidence:** 2017-08-04_delegation.md, 2018-02-10_force-multipliers.md, 2020-09-07_forming-the-unicorn.md, 2025-02-28_should-managers-still-code.md

> "*A manager's output = the output of their organization + the output of the neighboring organizations under their influence.*" — 2017-08-04_delegation.md (and repeated verbatim across the corpus)

> "We'll begin by revisiting Andy Grove's equation for measuring a manager's impact, which states that *the output of a manager is the output of their team, plus the output of the neighboring teams under their influence*. This is always useful to refer to when thinking about how to spend your time. I contemplate it a lot." — 2025-02-28_should-managers-still-code.md

### Grow impact, not headcount — wartime, not peacetime

Best managers don't need more people. Reinforcements aren't coming. Measure managers on impact per engineer. Treat AI skeptics as underperformers.

**Recurring evidence:** 2024-12-29_2024-the-year-in-review.md, 2025-06-30_new-advice-for-aspiring-managers.md, 2018-02-10_force-multipliers.md, 2025-12-14_use-it-or-lose-it.md

> "In the current climate, which I see continuing into 2025, the best managers will be the ones that *don't* need more people to get the job done. They are running small, highly focused orgs that are able to ship quickly and efficiently." — 2024-12-29_2024-the-year-in-review.md

> "we need to measure ourselves as managers on the *impact per engineer* that we have." — 2024-12-29_2024-the-year-in-review.md

> "Whereas the previous focus of managers was to rapidly hire and scale their teams, today's focus is on expanding *impact*. This is because in today's macroeconomic environment, output is key." — 2025-06-30_new-advice-for-aspiring-managers.md

> "Becoming an active participant in your team sometimes means doing the things that don't scale. However, doing the things that don't scale is the way to be successful as a manager today." — 2025-12-14_use-it-or-lose-it.md

### Be in the details — middle management is not a comms bus

You need first-hand knowledge to be accountable. Use the probing-question test: what is each person working on, what's the estimate on project Y, what's the architecture of Z, what's the SLO status? If you can't answer, you're not in the details.

**Recurring evidence:** 2024-11-30_being-in-the-details.md, 2025-02-28_should-managers-still-code.md, 2025-12-14_use-it-or-lose-it.md

> "Middle management is *not* just a communication bus. You should be making things happen." — 2024-11-30_being-in-the-details.md

> "If you can't answer these questions, you're not in the details." — 2024-11-30_being-in-the-details.md

> "I would argue that being in the details is the key tenet of not just being a great manager in the climate that we find ourselves in, but also being a great manager *full stop*." — 2025-02-28_should-managers-still-code.md

> "I call this 'diving down the stack.' The idea is that you try as a manager to go one or two levels deeper than your team would typically expect. It should surprise them." — 2025-12-14_use-it-or-lose-it.md

### Look sideways, not just up and down — peer collaboration is the missing default

Middle management's natural outlook is vertical. The tragedy of the common leader is that middle managers compete for the shared manager's attention instead of cohering as peers. Senior leaders without trifectas become warring factions.

**Recurring evidence:** 2023-11-30_the-tragedy-of-the-common-leader.md, 2024-01-27_trifectas-go-all-the-way-up.md, 2017-09-25_your-network-inside-the-business.md, 2025-08-30_going-direct.md, 2024-10-30_solving-staffing-challenges-with.md

> "the default *outlook* for middle management is to look up and down the org chart, but not sideways." — 2023-11-30_the-tragedy-of-the-common-leader.md

> "the senior leaders are isolated from each other as part of warring factions, leading to dysfunctional behavior" — 2024-01-27_trifectas-go-all-the-way-up.md

> "So, go direct. The org chart does not control the flow of communication. In fact, you're faster if you ignore it entirely." — 2025-08-30_going-direct.md

### Process is code — refactor it, delete it, let those closest change it

Processes go stale like code. The people executing them every day know best. Let chaos reign during the unknown; codify only what survives.

**Recurring evidence:** 2018-11-01_process.md, 2018-01-15_management-bugs.md, 2018-12-13_management-bugs-18-months-later.md, 2018-03-27_engineering-at-scale-is-a-people-problem.md

> "Processes, like code, shouldn't be set in stone. They should be revisited, tweaked, refactored, rewritten and deleted." — 2018-11-01_process.md

> "A process should fundamentally serve those that are continually applying it. If those closest to the ground want to make it better, then they should absolutely be allowed to change that process *for themselves*." — 2018-11-01_process.md

> "If we're not careful then we can end up layering more and more complexity on top of what are essentially *people problems* and then inadvertently create *even more* people problems as a result. It's a vicious circle." — 2018-03-27_engineering-at-scale-is-a-people-problem.md

### Performance management is the rising tide

Performance management isn't admin. It's about ensuring the organization is getting better every week, month, year. Staying the same is stagnation, not good performance. Effective systems positively compound; absent ones compound negatively.

**Recurring evidence:** 2024-03-31_performance-management-the-rising.md, 2017-08-24_performance-reviews.md, 2017-12-12_the-contribution-curve.md, 2018-08-30_dont-make-your-staff-afraid-to-fail.md

> "Performance management isn't primarily about checking that everyone is doing OK, nor is it primarily about ensuring that everyone is fairly compensated (although these are second-order effects): it's about ensuring that your organization is getting better every week, month, and year." — 2024-03-31_performance-management-the-rising.md

> "An effective performance management system, applied consistently, *positively compounds whole company performance over time*." — 2024-03-31_performance-management-the-rising.md

> "The bottom line is that this is the most important commitment, so everything else, within reason, moves out of the way." — 2017-08-24_performance-reviews.md

### Keep strategy alive with heartbeats

Strategies get written once and forgotten. Communication of the strategy is only the first step. Quarterly/biannual heartbeats turn it from academic exercise into evidence of progress — and bring everyone along through proof.

**Recurring evidence:** 2024-08-26_heartbeats-keeping-strategies-alive.md, 2024-02-29_parkinsons-law-its-real-so-use-it.md, 2025-04-29_a-weekly-mind-meld.md

> "Too many good strategies get written once and then forgotten about, collecting digital dust in a document somewhere. Creating and communicating the strategy is only the first step of the work" — 2024-08-26_heartbeats-keeping-strategies-alive.md

> "keeping it alive with regular heartbeats is where you bring *everyone else along through proof.*" — 2024-08-26_heartbeats-keeping-strategies-alive.md

> "humans *always* underestimate what they can get done in one week. See how many teams, projects, and tasks that you can inject a weekly reporting cadence into" — 2024-02-29_parkinsons-law-its-real-so-use-it.md

### Manage your managers as interfaces

Define what each manager must implement (KPIs, processes, rituals) without dictating how. Co-design the interface up front, then let them choose the implementation. When something goes wrong, attach the debugger to the agreed methods.

**Recurring evidence:** 2020-08-23_managing-through-interfaces.md, 2017-08-04_delegation.md, 2024-10-30_solving-staffing-challenges-with.md

> "**As a manager of managers, you define what the interface that represents each of your teams looks like.**... **Each of your managers has the flexibility of deciding exactly how those teams are run, as long as they follow the interface contract.**" — 2020-08-23_managing-through-interfaces.md

> "Clear interfaces allow you to not have to worry about the exact implementation details of how each of your managers run their teams, but they allow you to make it clear *exactly what you expect of each of them in doing so, and therefore how you define success*." — 2020-08-23_managing-through-interfaces.md

> "you are implicitly coaching your managers that you do not need to be the arbiter of all staffing challenges and that they should be working with their peers to solve these problems *themselves* with the trade-offs that they need to make." — 2024-10-30_solving-staffing-challenges-with.md

### Force multipliers — three categories of leverage

When you can't grow headcount or get promoted, you can still multiply impact in three orthogonal ways: technical (skills go further), cultural (improve the climate), procedural (better processes for everyone).

**Recurring evidence:** 2018-02-10_force-multipliers.md, 2024-12-29_2024-the-year-in-review.md, 2025-12-14_use-it-or-lose-it.md

> "There are three broad categories: * **Technical:** You can make your technical skills go further... * **Cultural:** You can focus on improving the culture of the department... * **Procedural:** You can focus on making department-wide processes better" — 2018-02-10_force-multipliers.md

### Don't make yourself redundant when you scale up

When splitting a team, promote/hire one new EM and run the other half yourself. Don't promote two new EMs and become a pure two-person manager-of-managers — you'll have delegated all your responsibility and entered on-the-job retirement.

**Recurring evidence:** 2020-09-27_dont-make-yourself-redundant.md, 2020-10-04_delegation-creates-career-progression.md, 2020-08-15_vp-director-what.md

> "The manager that is splitting the team should instead promote or hire one EM to run one of the sub-teams, then *run the other team themselves* by *acting* as the EM even though they've moved up into a Director of Engineering role." — 2020-09-27_dont-make-yourself-redundant.md

> "**Our new Director of Engineering has made themselves redundant.** By going from managing too many people to just 2, they've delegated all of their responsibility without the existence of other impactful activities that they can fill their time with. They've entered *on the job retirement.*" — 2020-09-27_dont-make-yourself-redundant.md

## Communication, writing & remote work

### Writing is the highest-leverage skill

Writing is a normalising medium — a pure transfer of ideas with no judgement based on creed, colour, age or gender. A considered written argument almost always beats an unprepared spoken one. The way to get better at writing is to write.

**Recurring evidence:** 2018-07-12_the-importance-of-writing.md, 2022-07-10_how-do-i-get-better-at-writing.md, 2021-02-04_the-spectrum-of-synchronousness.md, 2018-06-08_why-i-couldnt-write-a-manager-readme.md

> "Writing is a normalizing medium. No matter what you look like, how old you are, how you speak, or how confident you are, you can sit on your own and formulate your thoughts, draft and re-edit, and when you're done, they can be presented in the same standard form as Bezos, Hemingway or Dickens: words on the page; a pure transfer of ideas from one brain to another with no judgement or discrimination based on creed, color, age or gender." — 2018-07-12_the-importance-of-writing.md

> "**The way to get better at writing is to write.** And those that are able to access that flow state and produce text with the ability to self critique will improve." — 2022-07-10_how-do-i-get-better-at-writing.md

> "Consider this: what's one of the most impactful skills that you can improve as an engineer? Is it your programming? Maybe it's your debugging? I'd like to make the case that it's your *communication*." — 2021-02-04_the-spectrum-of-synchronousness.md

### Shift right — every interaction is an async opportunity

Sync/async isn't binary; it's a continuum from face-to-face to wikis. In every interaction, deliberately move one step toward more asynchronous communication. Habitually produce artifacts.

**Recurring evidence:** 2021-02-04_the-spectrum-of-synchronousness.md, 2021-02-18_the-spectrum-of-permanence.md, 2021-01-20_treat-everyone-as-remote.md

> "There's another important distinction to be made first: it isn't a binary choice between the two modes. It's a *continuum*." — 2021-02-04_the-spectrum-of-synchronousness.md

> "Every single interaction is an opportunity to shift right, and by doing so you are having much more of a dramatic impact than you may think." — 2021-02-04_the-spectrum-of-synchronousness.md

> "**Habitually produce artifacts.** With everything that you do, ask the question as to whether you should be creating a useful artifact for the future." — 2021-01-20_treat-everyone-as-remote.md

### Treat everyone as remote — broadcast at the widest useful level

Default every interaction to a remote-friendly mode so co-located staff don't accidentally become a privileged in-group. Don't repeat a piece of info in a DM, team chat and dept chat — go straight to the widest applicable audience.

**Recurring evidence:** 2021-01-20_treat-everyone-as-remote.md, 2018-11-08_switching-to-a-remote-manager.md, 2020-10-18_if-youre-repeating-yourself-debug-it.md, 2019-01-31_how-to-share-just-enough-information.md

> "That's how you solve the problem of any worker in your company feeling like they are 'remote'. You simply act as if everyone is, thus cancelling out the prefix: if *everyone* is treated like a remote worker, then really, they're all just *workers*." — 2021-01-20_treat-everyone-as-remote.md

> "**Broadcast information to the widest possible group.** Think about who is hearing, seeing and reading your communication. Could it be useful to a broader group of participants, even if it's just optional information that they can read if they're interested?" — 2021-01-20_treat-everyone-as-remote.md

> "However, when it comes to *communication*, managers find themselves writing that metaphorical code again and again and again, without necessarily thinking that there could be a better way to operate. There almost always is." — 2020-10-18_if-youre-repeating-yourself-debug-it.md

### In the absence of information, people assume the worst

Silence breeds bad rumours. Default to broadcasting the *existence* of work even when the details must stay private. Closed-box, not invisible.

**Recurring evidence:** 2019-01-31_how-to-share-just-enough-information.md, 2017-10-18_wobble.md

> "In the absence of information, people tend to assume the worst. So try not to let that information be absent in the first place." — 2019-01-31_how-to-share-just-enough-information.md

> "My own take is that the *existence* of closed box information should be broadcast as much as is useful for everyone's knowledge, except that the details are not disclosed." — 2019-01-31_how-to-share-just-enough-information.md

### Run a weekly mind meld with the team

A regular written update from a leader to close the gap between their thinking and the team's. 60 minutes max, 1,500 words max. Tag material as you go through the week; aggregate on Friday. Writing is the most scalable form of senior-leader communication.

**Recurring evidence:** 2025-04-29_a-weekly-mind-meld.md, 2018-11-08_switching-to-a-remote-manager.md, 2024-02-29_parkinsons-law-its-real-so-use-it.md, 2024-08-26_heartbeats-keeping-strategies-alive.md

> "It's how I continually open up my thoughts to the team with a long-term goal to reduce any mental alignment gap between us. I like to think that the more I share, the more they can understand what I believe is important and why, and the more that my style of working and thinking can propagate through the team." — 2025-04-29_a-weekly-mind-meld.md

> "Even though writing isn't video or audio, I still think it's the most scalable way to communicate with a large team, and one that allows me to keep pushing forward on the things that I believe are important, whilst keeping the team aligned and informed." — 2025-04-29_a-weekly-mind-meld.md

> "I needed to take the position of a screenwriter of a soap opera: an inventor of a regular rolling feed of narrative that is easy to soak in, letting the reader learn the characters and plot lines gradually by osmosis." — 2018-11-08_switching-to-a-remote-manager.md

### Pick the right medium for the conversation

Email is good for archival, newsletters, narrow-focus discussion and ratifying decisions. Bad for hot multi-author threads or urgent matters. A flurry of email is a signal to jump into chat, video or a shared doc.

**Recurring evidence:** 2018-08-02_that-massive-email.md, 2021-02-04_the-spectrum-of-synchronousness.md, 2018-11-08_switching-to-a-remote-manager.md

> "**Conversations with many active authors.**... begin to feel like a series of sliding doors. Everything gets confusing, communication is poor, effort is wasted, and nobody gets anything done. Consider a flurry of email thread activity as a signal to jump in a Slack channel, or do a video call, or start a shared document." — 2018-08-02_that-massive-email.md

> "you can specify the actions that you want the readers to take, even if those actions are just to read it and do nothing else." — 2018-08-02_that-massive-email.md

## The AI-era operator

### Trade headcount for tooling

The floor of developer productivity is rising. Buy subscriptions before you hire. Productivity gains from an existing team will more than make up for budget growth — and you owe employees the best tools.

**Recurring evidence:** 2025-03-30_llms-an-operators-view.md, 2025-06-30_new-advice-for-aspiring-managers.md, 2024-12-29_2024-the-year-in-review.md, 2025-09-30_the-beauty-of-constraints.md

> "As an operator, up-skilling your team to use these tools is now *essential*. Securing the necessary budget to give everyone access to the Pro tiers of ChatGPT, Cursor, or whatever tools represent the best fit for your team is a table stakes activity. And yes, this does mean that your budget will increase, but the productivity gains from an existing team will more than make up for it. Trade the cost of hiring new people for the cost of acquiring tooling." — 2025-03-30_llms-an-operators-view.md

> "Software development isn't just changing, it *has* changed, and if you haven't been adapting already, you're getting left behind. This isn't just important for your company, but it's also incredibly important for your employees: you owe them access to the best tools available to do their jobs." — 2025-03-30_llms-an-operators-view.md

> "Whereas new hires flowed liberally in the past, meaning that future roadmaps were built on the assumption that more people would be available to do the work, today, headcount is *heavily* scrutinized." — 2025-06-30_new-advice-for-aspiring-managers.md

### LLM as co-processor — pair-prompt your thinking

An LLM is a second processor that puts momentum behind your thinking and exposes alternative perspectives. Keep it physically visible. Use it as a contrarian advisor explicitly. Build councils of agents (PM, security, principal engineer) to compress two real meetings of iteration into one local session.

**Recurring evidence:** 2025-07-31_leadership-co-processing-with-llms.md, 2025-05-31_a-bag-of-worries.md, 2025-10-30_councils-of-agents.md, 2026-04-23_my-cto-daily-driver.md

> "Effectively, I now think of LLMs as a co-processor for my brain. It isn't always correct or even trustworthy, but in practice it always puts momentum behind my thinking, and often helps me to see things from a different perspective." — 2025-07-31_leadership-co-processing-with-llms.md

> "Pair prompting is just like pair programming, but with an LLM as the third member of the team. The idea is that you and your partner can use the LLM to help you both think through a problem together, and it can help you to see things from a different perspective." — 2025-07-31_leadership-co-processing-with-llms.md

> "You can use agents to form specific thinking councils that you can use to accelerate your thinking faster than you could by working either on your own or by requiring synchronous time with others." — 2025-10-30_councils-of-agents.md

> "Sometimes the act of maintaining fast, synchronous connections with groups of people in order to debate, discuss, and forward your thinking can be blocked by others' busyness or timezone. That's where agents come in." — 2025-10-30_councils-of-agents.md

### Be the surgeon, not the passenger — don't outsource understanding

AI is the team of assistants; you make the key decisions. Don't become a passenger in your own org. Always take a first pass yourself before bringing AI in. When the model gives you an answer, trace the code path.

**Recurring evidence:** 2025-12-14_use-it-or-lose-it.md, 2026-04-13_who-will-be-the-senior-engineers.md, 2026-03-13_slow-down-to-speed-up.md

> "Here, Geoffery Litt (referencing a theme covered in The Mythical Man-Month) argues that we should be the surgeon, making the key decisions and actions, and the AI should be the team of assistants, allowing us to delegate the grunt work." — 2025-12-14_use-it-or-lose-it.md

> "But, as more of us offload our strategic thinking and planning to AI... there is a risk of these core cognitive managerial skills diminishing too, and as such, we need to be careful. We mustn't become passengers in our own orgs." — 2025-12-14_use-it-or-lose-it.md

> "Don't outsource your understanding. AI tools are incredible accelerators, but they can also become a crutch. When the model gives you an answer, take the time to understand why it works. Read the documentation. Trace the code path." — 2026-04-13_who-will-be-the-senior-engineers.md

### Skeptical, not cynical — treat AI skeptics as underperformers

It has never been a better time to be a software engineer. Cynicism is awful for you, your team and your company. Refusing AI is now a performance issue, not a preference.

**Recurring evidence:** 2024-12-29_2024-the-year-in-review.md, 2025-06-30_new-advice-for-aspiring-managers.md

> "Be skeptical, but don't be cynical. It has never been as good as it has been now to be a software engineer." — 2024-12-29_2024-the-year-in-review.md

> "Likely treat AI skeptics as underperformers. Although it makes me feel somewhat uncomfortable writing this, there really is no place for people who refuse to use AI in today's software engineering roles: it is evident that productivity is significantly higher when it is used, and so it is a key part of *your* job to ensure that your team is using it effectively." — 2025-06-30_new-advice-for-aspiring-managers.md

### Adoption is organic — beware the productivity J-curve

For 99% of companies, mandated AI adoption costs more talent than it gains. The lag isn't tech failure; it's the time orgs need to rethink processes. Stop using new tech to do old things faster.

**Recurring evidence:** 2025-12-18_how-do-i-get-everyone-to-use-ai.md, 2025-03-30_llms-an-operators-view.md

> "But, as you know, that's perhaps 1%, maybe less, of companies out there. For everyone else, forcing adoption risks resentment, shadow non-compliance, and losing good people who feel micromanaged rather than empowered. The engineers who leave first are often the ones with options, who are also your best performers." — 2025-12-18_how-do-i-get-everyone-to-use-ai.md

> "The lag wasn't a failure of the technology; it was the time required for organizations to fundamentally rethink their processes. Companies had to stop using computers to do old things faster and start using them to do entirely new and better things. After all, nobody needs a faster horse." — 2025-12-18_how-do-i-get-everyone-to-use-ai.md

### Build the tools yourself

AI has democratised custom internal tooling. The right targets are problems too niche for anyone else to build for you. Perfect is the enemy of done; rough tools that solve your specific workflow are the point.

**Recurring evidence:** 2026-02-20_just-build-the-tools-yourself.md, 2026-04-23_my-cto-daily-driver.md, 2025-10-30_councils-of-agents.md

> "The problems worth solving this way are the ones too niche for anyone else to build for you: your specific workflow, your team's specific needs, the visibility gap that only matters in your context." — 2026-02-20_just-build-the-tools-yourself.md

> "It's not perfect, but it solves my problem well enough, and that's the point. Perfect is the enemy of done." — 2026-02-20_just-build-the-tools-yourself.md

> "A daily driver is something different: it's a personalised workspace that has memory, both internally via files and externally via other systems that act as sources of truth. It has your opinions baked in, and it's less a tool you pick up than an environment you quite literally drive your whole day from, one that only gets better with time." — 2026-04-23_my-cto-daily-driver.md

### Reviews matter more when generation is cheap

With AI shipping more code faster, the review process matters more, not less. If your most senior engineers' PRs were getting half-arsed thumbs-ups before, that won't survive the AI era. Bottlenecks shift when developers go faster.

**Recurring evidence:** 2025-03-30_llms-an-operators-view.md, 2025-02-28_should-managers-still-code.md, 2026-03-13_slow-down-to-speed-up.md

> "As such, with the faster production of code, as an operator it is more important than *ever* to ensure you have a strong review process in place: if your most senior engineers were getting a half-arsed rubber stamp thumbs up from their peers (not advised, but it happens), now you need to ensure that *all* code is being scrutinized as the origins of it are less clear." — 2025-03-30_llms-an-operators-view.md

> "Don't just skim PRs (sorry, reader!), but really dig into them: run the branch locally, test it, think critically about the design and the implementation, and provide feedback." — 2025-02-28_should-managers-still-code.md

> "Many companies are already at the point where they effectively block the speed of their own progress in other ways than just the number of developers they have. Making those developers faster may not actually help them ship more features, and in fact, it may make things worse." — 2025-03-30_llms-an-operators-view.md

### Juniors are R&D — protect scar tissue as a strategic asset

Senior judgement comes from shipping things that broke and staying up to fix them. AI can't give you scars. The middle of the career ladder is hollowing out — vibe coders at one end, deep engineers at the other. Treat junior hiring as investment, measure knowledge concentration like uptime.

**Recurring evidence:** 2026-04-13_who-will-be-the-senior-engineers.md, 2017-12-12_the-contribution-curve.md, 2018-08-30_dont-make-your-staff-afraid-to-fail.md

> "There's a term that comes to mind for how one progresses from junior to senior: *scar tissue*. The scars come from shipping something that broke in production and staying up to fix it, from proposing an architecture that didn't scale and having to rebuild it, from navigating a difficult stakeholder relationship and learning, the hard way, what actually works." — 2026-04-13_who-will-be-the-senior-engineers.md

> "On one side: vibe coders who move fast, shipping features by orchestrating AI tools, comfortable with velocity but shallow on fundamentals. On the other: engineers who understand how things actually work, but who are increasingly rare and expensive. The middle disappears." — 2026-04-13_who-will-be-the-senior-engineers.md

> "Treat junior hiring as R&D, not overhead. The return on investment isn't immediate, but it's real. Every junior you develop into a senior is institutional knowledge you don't lose when someone resigns." — 2026-04-13_who-will-be-the-senior-engineers.md

> "Measure your knowledge concentration. How many people on your team can debug your most critical systems? What's your bus factor on key services? If the answer is 'one or two,' you have a fragile organisation, regardless of how productive AI makes those individuals. Track knowledge distribution the way you track uptime." — 2026-04-13_who-will-be-the-senior-engineers.md

## Mental models

### Andy Grove's manager output equation

*A manager's output = the output of their team + the output of the neighboring organizations under their influence.* The e=mc² of management; use to interrogate where any minute of your time goes.

> "*A manager's output = the output of their organization + the output of the neighboring organizations under their influence.*" — 2017-08-04_delegation.md

### The three levers — scope, resources, time

Quality is off-limits. Everything else is negotiation across these three. Make trade-offs visible so scrutiny lands on pragmatic choices, not effort.

> "Now it goes without saying that you would not want to compromise on quality. I would argue that if you are happy with shipping poor quality software, then you are probably in the wrong job. Instead, you have three levers that you can adjust in order to find the right compromise with new projects. They are scope, resources, and time." — 2017-11-14_your-levers-scope-resources-and-time.md

### The Iron Triangle as a constraint toolkit

Same three levers, repurposed as offensive tools rather than defensive trade-offs. Constraints are your friend; the most over-budget late projects are the ones with the fewest constraints.

> "So the way that I encourage you to look at the iron triangle is not as an accepted set of trade-offs, but instead as a *toolkit of constraints* that are available to engineering leaders to help their teams deliver more with less." — 2025-09-30_the-beauty-of-constraints.md

### Radical Candor quadrant

Care personally × challenge directly. Failure modes: ruinous empathy (care, no challenge), obnoxious aggression (challenge, no care), manipulative insincerity (neither).

> "**Radical candor is what happens when you care personally and challenge someone directly.**" — 2022-07-24_how-do-i-get-better-at-giving-feedback.md

### Task-relevant maturity (Grove)

How skilled someone is at *this specific task*, not their job title. Calibrate delegation depth and oversight to TRM, not seniority.

> "Each member of staff in your organization has a level of seniority in their area or as Grove describes it, 'task-relevant maturity' (TRM). This is how skilled they are at getting tasks done to the required quality. Your approach to delegating is dependent on this skill level." — 2017-08-04_delegation.md

### The contribution curve

Every person sits on a curve from net-negative to net-positive contribution. The three causes of net-negative are different problems with different remedies: inexperience (training problem), poor placement (management problem), poor performance (performance problem).

> "**Inexperience:** The best case (if there has to be one). An individual needs education and mentorship to push through to being net-positive. This is a *training problem*. **Poor placement**: An individual is doing work that is either too challenging for them or they are unclear on how they should be effective in their role. This is a *management problem*. **Poor performance:** An individual is not performing well in their role, despite having the support that they need. This is a *performance problem*." — 2017-12-12_the-contribution-curve.md

### GROW model

Goal, Reality, Options, Wrap-up. A four-stage frame for any coaching conversation.

> "**Goal**: What's the goal of this session? What problem are we trying to solve? **Reality**: What's the situation like now? Who, what, where, and how much? **Options**: What are all of the different ways in which we can tackle this issue? **Wrap-up**: Become clear on a choice, commit to it, and discuss what support is needed." — 2017-12-21_coaching.md

### The wobble / the jelly

Emotional shocks at the top of the org chart cause much larger organisational wobble than the same shock lower down. Containing wobble is part of the senior manager's job. Listen → digest (sleep on it) → communicate.

> "The higher up the org chart, the bigger the potential organizational wobble." — 2017-10-18_wobble.md

### Force multipliers — technical, cultural, procedural

Three orthogonal categories of leverage when you can't grow headcount or get promoted.

> "There are three broad categories: * **Technical:** You can make your technical skills go further... * **Cultural:** You can focus on improving the culture of the department... * **Procedural:** You can focus on making department-wide processes better" — 2018-02-10_force-multipliers.md

### Stanier's Law of 1:1 entropy

With time and without conscious effort, all 1:1 meetings degenerate into status updates.

> "*With time, and without conscious effort, all 1 to 1 meetings will degenerate into status updates.* Can we call that Stanier's Law?" — 2018-05-18_keeping-your-1-to-1s-fresh.md

### Management bugs

Treat process and culture friction like software bugs: anyone files them publicly with their name, leadership triages and resolves them in the open. Stagnant bugs signal management doesn't care.

> "given it works for software bugs, why shouldn't we try something like this for process and management issues?" — 2018-01-15_management-bugs.md

### Chits

Flexibility (WFH, hours, time off, project choice) is an earned allowance, not a universal right. The best staff accumulate the most chits — and the link between performance and flexibility must be visible, or it looks like favouritism.

> "The more trustworthy and high-performing the employee, the more chits that they are allowed to have. This gives your best staff the most allowances, and sends a message that this flexibility is something that is *earned* and *not a right*." — 2018-02-27_chits.md

### The Tarzan Method — career as vine-swinging

Direct paths to senior roles don't exist. Trust instincts, swing to the next vine. Reframe the career question from "how do I get to the top fastest?" to "how do I maximise my chance of skyrocketing?"

> "Instead, you should think about your career like Tarzan swinging through the jungle. Tarzan starts at one tree and knows that he has an ultimate destination, but the path to get there isn't immediately clear" — 2024-04-23_the-tarzan-method.md

### Scope × Impact quadrant

Plot each role on (impact, scope). The four cells: Stagnating, Stepping up, Skyrocketing, Skilling up. Frame each Tarzan swing in terms of where it lands you.

> "On the x-axis, we have impact, and on the y-axis, we have scope. Given your own internal measurement of your current scope and impact, you can work out which quadrant applies to you in your current situation" — 2024-04-23_the-tarzan-method.md

### The Disappointment Frontier

The void formed from the mismatch between your team's desires and external reality. Bigger frontier = bigger explosion when reality collides with it. Leadership is shrinking it gradually, not hiding it.

> "The disappointment frontier is the void formed from the mismatch between your team and reality. The larger the frontier, the more potential for disappointment when reality collides with it." — 2024-05-24_the-disappointment-frontier.md

### Deltas to the global maxima

Career tracks describe local maxima of one company. Work backwards from the person's ideal future, define scope+impact for each step, calculate the delta between each.

> "Working backward from the global maxima, start defining scope and impact for each of the steps that you defined, and then calculate the delta between each of them." — 2024-06-25_deltas-to-the-global-maxima.md

### Thoroughness = scope + scalability + sustainability

The superset that lets you have a real trade-off discussion instead of "go faster." There's no magical way to just go faster — there's only picking a point on the thoroughness curve consciously.

> "I think of thoroughness as the superset of *scope*, *scalability*, and *sustainability*" — 2024-07-29_scope-hmm.md

### The Strategy Heartbeat

Quarterly or biannual structured update: recap → progress → impact → staffing → changes → looking forward. Keeps strategy from collecting digital dust.

> "One way to do this is to create a regular heartbeat for your strategy. The duration of this heartbeat is up to you, but aligning with one of the larger cycles of the year is a good bet: for example, perhaps you could do it quarterly or biannually." — 2024-08-26_heartbeats-keeping-strategies-alive.md

### Trifectas — Eng / Product / UX at every level

Cross-functional triads create positive tension. Senior leaders without trifectas become warring factions. Trifecta structure is independent of reporting lines.

> "One of the most powerful groups that you can be part of as a senior leader is a trifecta. A trifecta is a group of three people from different disciplines who work together to achieve a goal." — 2024-01-27_trifectas-go-all-the-way-up.md

### The Tragedy of the Common Leader

Middle managers compete for a shared manager's attention instead of cohering as peers. The polarity of your organization is determined by whether you generate value or conflict for other teams.

> "This is the tragedy of the common *leader*: despite you and your peer group having the same leader in common (i.e. access to the same resource), you act in your own self-interest, even if it is not in the group's long-term interest to do so." — 2023-11-30_the-tragedy-of-the-common-leader.md

### Gather-decide-execute

A continually-running three-phase loop that organizes a manager's day. Gathering is active, not passive — pull on threads, ask questions, fight skepticism decay.

> "I'll focus on the way using this tool allows me to categorize the way that I work into tight loops of *gathering, deciding, and executing*. This is a mental model that I've found to be very effective in managing my day-to-day work, and enables me to keep the pace high for myself and my team." — 2025-01-31_gather-decide-execute.md

### Bag of worries

Separate jumbled, larger worries from sequential actionable to-dos. Pluck one per day, often with the LLM, to unpack into a plan. Mental resistance, not task complexity, is usually the bottleneck.

> "As a result, I've separated out my to-do list into two parts: a 'to-do' list for actionable items, and a 'worries' list for these larger, more complex items that need more thought and planning." — 2025-05-31_a-bag-of-worries.md

### Going direct — context, problem, ask

A three-part structure for any request when bypassing reporting chains. Lateral or diagonal, not vertical. One-way door decisions escalate; everything else does not.

> "Encourage them to follow a simple structure: *context, problem, and a clear ask*." — 2025-08-30_going-direct.md

### Theory of Constraints applied to teams

Every system has exactly one constraint at any given time. Subordinate everything else to it. The question that finds the bottleneck: *what are we waiting on right now?*

> "The core insight is simple: every system, whether it's a factory or a software team, has exactly one constraint that limits its overall throughput at any given time." — 2026-01-14_one-bottleneck-at-a-time.md

### Inversion — invert, always invert

To succeed at an outcome, think about what would have to happen for you to fail, then avoid all those things. Bucket findings into showstopper / mitigation / accepted.

> "Munger adapts this into practical situations: to succeed at an outcome, you should invert it by thinking about what would have to happen for you to *fail*, and then completely avoid all of those things in order to succeed." — 2025-11-23_invert-always-invert.md

### Priority, not priorities — single-threaded leadership

The word was singular for 500 years. The plural lets us avoid hard choices. A single prioritised list is a forcing function. Anything important needs a leader entirely dedicated to it.

> "Amazon embodies this principle through what they call single-threaded leadership. David Limp, a former SVP, said: 'The best way to ensure that you failed to invent something is by making it somebody's part-time job.'" — 2026-02-13_one-list-to-rule-them-all.md

### A+ vs B+ problems (via Thiel)

People default to B+ problems they know how to solve. Discipline of one thing forces breakthroughs by stopping the natural drift to easier work.

> "A+ problems are high impact, but they're difficult, and you cannot immediately derive a solution, so you tend to procrastinate." — 2026-02-13_one-list-to-rule-them-all.md

### LLM as co-processor / pair prompting

A second processor for the brain. Always puts momentum behind your thinking. Pair prompting is pair programming with the LLM as a third member. Use as a contrarian advisor explicitly.

> "Effectively, I now think of LLMs as a co-processor for my brain." — 2025-07-31_leadership-co-processing-with-llms.md

### Surgeon, not passenger

You make key decisions; AI is the team of assistants. Use it or lose it: skills you don't practise daily decay. Find the minimum effective dose of coding to keep the skill alive.

> "Here, Geoffery Litt (referencing a theme covered in The Mythical Man-Month) argues that we should be the surgeon, making the key decisions and actions, and the AI should be the team of assistants, allowing us to delegate the grunt work." — 2025-12-14_use-it-or-lose-it.md

### The productivity J-curve

Adoption of new tech (printing press, PC, internet) dips into a trough before producing gains. The trough is normal and must be expected. Stop using new tech to do old things faster.

> "Humans have been through numerous productivity revolutions: the printing press, the Industrial Revolution, personal computing, the internet, and smartphones. For each of these technologies, adoption follows a J-curve." — 2025-12-18_how-do-i-get-everyone-to-use-ai.md

### Scar tissue

The judgement that comes from shipping things that broke. AI can't give you scars. Seek scar tissue deliberately: volunteer for on-call, take the messy migration nobody else wants.

> "The scars come from shipping something that broke in production and staying up to fix it, from proposing an architecture that didn't scale and having to rebuild it, from navigating a difficult stakeholder relationship and learning, the hard way, what actually works." — 2026-04-13_who-will-be-the-senior-engineers.md

### Daily driver — personalised AI workspace

Not a one-off session. A persistent workspace with memory, opinions baked in, integrations. Information flows: capture in inbox → triage into tasks/reference → execution in tracker → wins in brag doc → decisions logged.

> "A daily driver is something different: it's a personalised workspace that has memory, both internally via files and externally via other systems that act as sources of truth. It has your opinions baked in, and it's less a tool you pick up than an environment you quite literally drive your whole day from, one that only gets better with time." — 2026-04-23_my-cto-daily-driver.md

### Shoshin — beginner's mind for new contexts

When joining a new company, hold your expertise lightly. The trap is earned dogmatism: more expertise makes you more closed-minded. Principles transfer; prescriptions don't.

> "The antidote is something Zen Buddhists call *shoshin*, or *beginner's mind*: approaching a situation with openness and curiosity, even when you have experience. The goal isn't to pretend you don't know anything; it's to hold your expertise *lightly*, staying curious about what might be different in the here and the now." — 2026-03-20_new-company-old-playbook.md

## Context-only observations

Single-post claims that are interesting but do not meet the recurring-pattern bar. Kept for completeness; not load-bearing for the persona.

- **The Eye of Sauron** — that moment when the whole business turns its attention onto your team. Handle correctly = career growth; handle poorly = next high-stakes project goes elsewhere. — 2018-07-06_the-eye-of-sauron.md
- **Rockstars vs Superstars** — high performers split into stability-seekers (rockstars, protect from change) and change-seekers (superstars, throw at pivot points). Via Kim Scott. — 2017-09-29_rockstars-and-superstars.md
- **Mount Stupid** — Dunning-Kruger in the workplace. You won't know when you're on it. Defuse with offline + written presentation of facts, not in-person ego clashes. — 2017-12-05_mount-stupid.md
- **A fistful of radishes** — you can only teach what you know; surround yourself with people unlike you so your biases get challenged. — 2018-10-25_radishes.md
- **Span of control modes** — 1-2 reports = redundant manager, 3-6 = hands-on, 5-10 = sweet spot, 12-15 = coordinator, 15+ = diminished. Sweet spot ~8 (caveated heavily). — 2023-09-24_how-many-direct-reports-should-a.md
- **Trichotomy of control** (vs Stoic dichotomy) — full control / no control / partial control. For partial control, measure against an internal goal not an external outcome. — 2018-09-27_the-trichotomy-of-control.md
- **The peloton, not the broom wagon** — your role as a new manager is at the front of the peloton, not sweeping up behind the team. — 2018-03-03_letting-go.md
- **The hoisted Principal Engineer** — promote your best senior engineers *out* of teams to report directly to you so they can lead engineering-driven, cross-team work. — 2019-02-14_who-could-be-your-jeff-dean.md
- **Concentric circles for staffing** — solve inside-out: team → neighbours → broader org → department. Implicitly coaches managers that you aren't the staffing arbiter. — 2024-10-30_solving-staffing-challenges-with.md
- **Tactical / Operational / Strategic** — EMs operate tactically, Directors operationally, VPs strategically. Borrowed from military doctrine. — 2020-08-15_vp-director-what.md
- **Manager Voltron** — build a peer network around your reports that fills the gaps you can't fill (via Lara Hogan). — 2020-09-07_forming-the-unicorn.md
- **The spectrum of humanity** — async work makes you efficient but can leave you hollow. Sometimes deliberately use the "wrong" (synchronous, inefficient) format on purpose. Encourage goofing off on work time. — 2021-03-17_the-spectrum-of-humanity.md
- **Soap opera not novel** — weekly written digest to a remote manager should be a rolling narrative absorbed by osmosis, not a complete documentation effort. — 2018-11-08_switching-to-a-remote-manager.md
- **Distilling personas as synthetic advisors** — turn interviews/podcasts/talks of admired leaders into a queryable role. Pair with a "mirror" run on your own writing to surface your real principles. — 2026-05-15_distilling-leadership-wisdom.md
- **Random walk career / map not blueprint** — careers follow curiosity; share the path as terrain, not template. Different interests as differentiation; trust your gut. — 2025-11-26_my-path-to-cto-part-i.md
