create table public.story_comments (
  id uuid primary key,
  story_id text not null check (story_id ~ '^story-[a-zA-Z0-9_-]{1,100}$'),
  body text not null check (char_length(body) between 3 and 600),
  created_at timestamptz not null default now()
);
create index story_comments_story_created_idx on public.story_comments (story_id, created_at desc);
alter table public.story_comments enable row level security;
revoke all on public.story_comments from public, anon, authenticated;
grant select on public.story_comments to anon, authenticated;
grant select, insert on public.story_comments to service_role;
create policy "Read published comments" on public.story_comments for select to anon, authenticated using (true);

create table public.story_comment_rate (
  bucket timestamptz primary key,
  attempts integer not null
);
alter table public.story_comment_rate enable row level security;
revoke all on public.story_comment_rate from public, anon, authenticated;
grant select, insert, update, delete on public.story_comment_rate to service_role;

create function public.reserve_story_comment()
returns boolean language plpgsql security invoker set search_path = '' as $$
declare
  current_bucket timestamptz := date_trunc('minute', now());
  allowed boolean;
begin
  delete from public.story_comment_rate where bucket < current_bucket - interval '1 hour';
  insert into public.story_comment_rate as rate (bucket, attempts) values (current_bucket, 1)
  on conflict (bucket) do update set attempts = rate.attempts + 1 where rate.attempts < 20
  returning true into allowed;
  return coalesce(allowed, false);
end;
$$;
revoke all on function public.reserve_story_comment() from public, anon, authenticated;
grant execute on function public.reserve_story_comment() to service_role;
