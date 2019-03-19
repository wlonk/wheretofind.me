import iconGuesses from '@/iconGuesses';

describe('iconGuesses', () => {
  test.each([
    ['behance.net'],
    ['blogger.com'],
    ['bitbucket.org'],
    ['codepen.io'],
    ['deviantart.com'],
    ['discordapp.com'],
    ['dribbble.com'],
    ['ello.co'],
    ['etsy.com'],
    ['facebook.com'],
    ['github.com'],
    ['gitlab.com'],
    ['goodreads.com'],
    ['instagram.com'],
    ['keybase.io'],
    ['kickstarter.com'],
    ['last.fm'],
    ['medium.com'],
    ['patreon.com'],
    ['paypal.com'],
    ['pinterest.com'],
    ['plus.google.com'],
    ['ravelry.com'],
    ['reddit.com'],
    ['skype.com'],
    ['slack.com'],
    ['snapchat.com'],
    ['soundcloud.com'],
    ['stackoverflow.com'],
    ['steamcommunity.com'],
    ['teamspeak.com'],
    ['tumblr.com'],
    ['twitch.tv'],
    ['twitter.com'],
    ['untappd.com'],
    ['vimeo.com'],
    ['youtube.com'],
    ['pora'],
    ['mastodon'],
  ])('finds %s', url => {
    const matches = iconGuesses
      .map(el => {
        const { fn } = el;
        return fn(`https://${url}/`);
      })
      .filter(el => el);

    expect(matches.length).toEqual(2);
  });

  test('tests fallthrough truly', () => {
    const url = 'example.com';
    const matches = iconGuesses
      .map(el => {
        const { fn } = el;
        return fn(`https://${url}/`);
      })
      .filter(el => el);

    expect(matches.length).toEqual(1);
  });

  test('tests mailto truly', () => {
    const address = 'mailto:test@example.com';
    const matches = iconGuesses
      .map(el => {
        const { fn } = el;
        return fn(address);
      })
      .filter(el => el);

    expect(matches.length).toEqual(2);
  });
});
