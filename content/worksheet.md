# Pick Your First Project

Answer a few quick questions. No data leaves your browser — this page is a
little script that runs locally and suggests a match from this directory,
plus a gentle plan for your first week. You can change your answers and
re-run as often as you like.

<div class="worksheet" id="worksheet">

<div class="ws-q">
  <p><strong>1. How much time can you honestly give this week?</strong></p>
  <label><input type="radio" name="time" value="tiny" checked> Little sips — under 30 minutes, whenever a window opens</label>
  <label><input type="radio" name="time" value="hour"> About an hour, once or twice this week</label>
  <label><input type="radio" name="time" value="committed"> I can commit to training and regular hours</label>
</div>

<div class="ws-q">
  <p><strong>2. Do you want to talk to people?</strong></p>
  <label><input type="radio" name="people" value="no" checked> Not really — let me work alone</label>
  <label><input type="radio" name="people" value="typing"> Text/chat is fine</label>
  <label><input type="radio" name="people" value="voice"> Yes — calls, video, or live sessions</label>
</div>

<div class="ws-q">
  <p><strong>3. Which sounds more like you this month?</strong></p>
  <label><input type="radio" name="mode" value="head" checked> Quiet focus: reading, typing, puzzling things out</label>
  <label><input type="radio" name="mode" value="hands"> Making things with my hands</label>
  <label><input type="radio" name="mode" value="fixing"> Clicking around apps and sites and noticing what bugs me</label>
</div>

<div class="ws-q">
  <p><strong>4. Are you 18 or older?</strong></p>
  <label><input type="radio" name="adult" value="adult" checked> Yes</label>
  <label><input type="radio" name="adult" value="teen"> Not yet (or I'm picking for a teen)</label>
</div>

<p><button type="button" id="ws-run" class="ws-btn">Show my match</button></p>

<div id="ws-result" class="ws-result" hidden></div>

</div>

## How the worksheet picks

The script scores each of the six directory entries against your answers and
shows the best fit with an honest note about why. It is deliberately simple:
it applies the same guidance the entries give in plain language — age rules,
training time, whether you interact with people — and it is meant to get you
*started*, not to seal your fate. If the first match doesn't feel right, run
it again or just pick the second-place suggestion.
