FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Next.js inlines NEXT_PUBLIC_* into the client bundle at BUILD time, so the
# value must exist here (api.ts falls back to "" = same-origin, which is what
# prod wants behind Caddy). Dev passes it via build.args in docker-compose.yml.
ARG NEXT_PUBLIC_API_URL=""
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

CMD ["npm", "start"]
