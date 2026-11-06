# The exercise: a job runner

Build a small job runner out of three services. `README.md` explains how the exercise is run and what limits apply. This
file says what to build. `openapi.yaml` is the contract for the API; where this file and `openapi.yaml` differ,
`openapi.yaml` wins.

## What to build

- `api` stores the jobs that are submitted to it in Postgres and serves them back.
- `worker` claims the jobs that `api` stored and runs them.
- `web` shows each job's state and updates without a page reload.

The kit gives you a stub of each service in `services/`. The stubs start and stop correctly, and `api` checks that it can
reach Postgres. They do nothing else. Replace them with your own.

## The job type

There is one job type, `sleep`. A `sleep` job succeeds `payload.duration_ms` milliseconds after a worker starts it.

A job's status moves from `queued` to `running`, then to `succeeded` or `failed`. It never moves backwards.

A job has these fields:

| Field | Value |
| --- | --- |
| `id` | A string that is unique for each job |
| `type` | `sleep` |
| `payload` | `{"duration_ms": <integer>}` |
| `status` | `queued`, `running`, `succeeded` or `failed` |
| `error` | A string when the job failed, otherwise `null` |
| `created_at` | A date-time, set when the job is stored |
| `started_at` | A date-time when a worker started the job, otherwise `null` |
| `finished_at` | A date-time when the job finished, otherwise `null` |

A finished job looks like this:

```json
{
  "id": "5b0f4c9e-6a1d-4f64-8d1e-3c0a1e7d9b22",
  "type": "sleep",
  "payload": {"duration_ms": 500},
  "status": "succeeded",
  "error": null,
  "created_at": "2026-10-06T14:00:00.000Z",
  "started_at": "2026-10-06T14:00:00.250Z",
  "finished_at": "2026-10-06T14:00:00.752Z"
}
```

Write times with enough precision that `finished_at` minus `started_at` is at least `duration_ms`.

## The API

`api` listens on port 8000 and answers every route as JSON.

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| `GET` | `/healthz` | The API is up and can query Postgres | `200` |
| `POST` | `/jobs` | Submit a job with the body `{"type":"sleep","payload":{"duration_ms":<n>}}` | `201` with the job |
| `GET` | `/jobs/{id}` | One job | `200` with the job |
| `GET` | `/jobs` | All jobs | `200` with `{"jobs":[...]}` |

## The web page

`web` listens on port 3000 and answers `GET /` with an HTML page. The page shows each job's state and updates without a
reload, so a person watching sees a job go from `queued` to `running` to `succeeded`.

## The database

Postgres starts empty. Your services create their own schema. Reach it through `DATABASE_URL` and nowhere else.

## The smoke test

After your stack is up, Pairwise runs a smoke test against it. The test image is public, and `./pw-check` runs the same
one. It has five checks:

1. `healthz`: `GET /healthz` on `api` returns `200`.
2. `submit_jobs`: five `POST /jobs` calls with a `sleep` job of 500 ms each return `201` with a job.
3. `jobs_succeed`: each of those jobs reaches `succeeded` within 30 s of being submitted, and
   `finished_at` minus `started_at` is at least `duration_ms`.
4. `list_jobs`: `GET /jobs` lists those jobs as `succeeded`.
5. `web_page`: `GET /` on `web` returns `200` as `text/html`.

Passing the smoke test is the start, not the whole of the exercise. Your own tests, `DESIGN.md` and `AI-USAGE.md` matter
too.
